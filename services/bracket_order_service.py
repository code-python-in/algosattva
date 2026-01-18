"""
Bracket Order Service

This service implements bracket order functionality that:
1. Places an entry order at the specified price
2. Upon confirmation, places a GTT OCO (One Cancels Other) order for SL and Target
"""

import importlib
import traceback
import copy
import time
from typing import Tuple, Dict, Any, Optional
from threading import Thread

from database.auth_db import get_auth_token_broker
from database.apilog_db import async_log_order, executor
from database.settings_db import get_analyze_mode
from database.analyzer_db import async_log_analyzer
from extensions import socketio
from utils.api_analyzer import analyze_request, generate_order_id
from utils.constants import (
    VALID_EXCHANGES,
    VALID_ACTIONS,
    VALID_PRICE_TYPES,
    VALID_PRODUCT_TYPES,
)
from utils.logging import get_logger
from services.telegram_alert_service import telegram_alert_service

# Initialize logger
logger = get_logger(__name__)


def import_broker_module(broker_name: str) -> Optional[Any]:
    """
    Dynamically import the broker-specific order API module.

    Args:
        broker_name: Name of the broker

    Returns:
        The imported module or None if import fails
    """
    try:
        module_path = f'broker.{broker_name}.api.order_api'
        broker_module = importlib.import_module(module_path)
        return broker_module
    except ImportError as error:
        logger.error(f"Error importing broker module '{module_path}': {error}")
        return None


def validate_bracket_order(order_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate bracket order data

    Args:
        order_data: Order data to validate

    Returns:
        Tuple containing:
        - Success status (bool)
        - Error message (str) or None if validation succeeded
    """
    # Required fields for bracket order (apikey is validated separately)
    required_fields = ['symbol', 'exchange', 'product', 'action', 'quantity', 'entry_price', 'sl_price', 'target_price']

    # Check for missing mandatory fields
    missing_fields = [field for field in required_fields if field not in order_data]
    if missing_fields:
        return False, f'Missing mandatory field(s): {", ".join(missing_fields)}'

    # Validate exchange
    if order_data['exchange'] not in VALID_EXCHANGES:
        return False, f'Invalid exchange. Must be one of: {", ".join(VALID_EXCHANGES)}'

    # Convert action to uppercase and validate
    action = order_data.get('action', '').upper()
    if action not in ['BUY', 'SELL']:
        return False, f'Invalid action. Must be BUY or SELL (case insensitive)'

    # Validate quantity
    try:
        quantity = int(order_data.get('quantity', 0))
        if quantity <= 0:
            return False, 'Quantity must be greater than 0'
    except (ValueError, TypeError):
        return False, 'Invalid quantity'

    # Validate prices
    try:
        entry_price = float(order_data.get('entry_price', 0))
        sl_price = float(order_data.get('sl_price', 0))
        target_price = float(order_data.get('target_price', 0))

        if entry_price <= 0:
            return False, 'Entry price must be greater than 0'
        if sl_price <= 0:
            return False, 'SL price must be greater than 0'
        if target_price <= 0:
            return False, 'Target price must be greater than 0'

        # Validate SL and Target relative to entry price
        if action == 'BUY':
            if sl_price >= entry_price:
                return False, 'For BUY orders, SL price must be less than entry price'
            if target_price <= entry_price:
                return False, 'For BUY orders, target price must be greater than entry price'
        else:  # SELL
            if sl_price <= entry_price:
                return False, 'For SELL orders, SL price must be greater than entry price'
            if target_price >= entry_price:
                return False, 'For SELL orders, target price must be less than entry price'

    except (ValueError, TypeError):
        return False, 'Invalid price values'

    # Validate product type if provided
    if 'product' in order_data and order_data['product'] not in VALID_PRODUCT_TYPES:
        return False, f'Invalid product type. Must be one of: {", ".join(VALID_PRODUCT_TYPES)}'

    return True, None


def place_bracket_order_with_auth(
    order_data: Dict[str, Any],
    auth_token: str,
    broker: str,
    original_data: Dict[str, Any],
) -> Tuple[bool, Dict[str, Any], int]:
    """
    Place a bracket order with entry order and GTT OCO for SL and Target.

    Args:
        order_data: Bracket order data
        auth_token: Authentication token for the broker API
        broker: Name of the broker
        original_data: Original request data for logging

    Returns:
        Tuple containing:
        - Success status (bool)
        - Response data (dict)
        - HTTP status code (int)
    """
    order_request_data = copy.deepcopy(original_data)
    if 'apikey' in order_request_data:
        order_request_data.pop('apikey', None)

    # Validate bracket order data
    is_valid, error_message = validate_bracket_order(order_data)
    if not is_valid:
        error_response = {'status': 'error', 'message': error_message}
        executor.submit(async_log_order, 'placebracketorder', original_data, error_response)
        return False, error_response, 400

    # Live Mode - Proceed with actual order placement
    broker_module = import_broker_module(broker)
    if broker_module is None:
        error_response = {
            'status': 'error',
            'message': 'Broker-specific module not found'
        }
        executor.submit(async_log_order, 'placebracketorder', original_data, error_response)
        return False, error_response, 404

    try:
        # Step 1: Place the entry order
        entry_order_data = {
            'symbol': order_data['symbol'],
            'exchange': order_data['exchange'],
            'product': order_data['product'],
            'action': order_data['action'].upper(),
            'quantity': str(order_data['quantity']),
            'price': str(order_data['entry_price']),
            'pricetype': 'LIMIT',
            'ordertype': 'REGULAR',
        }

        logger.info(f"Placing entry order: {entry_order_data}")

        # Call the broker's place_order_api
        res, response_data, order_id = broker_module.place_order_api(entry_order_data, auth_token)

        if res is None or res.status != 200:
            error_msg = response_data.get('message', 'Failed to place entry order')
            error_response = {
                'status': 'error',
                'message': f'Entry order failed: {error_msg}'
            }
            executor.submit(async_log_order, 'placebracketorder', original_data, error_response)
            logger.error(f"Entry order placement failed: {error_msg}")
            return False, error_response, 400

        # Log the entry order placement
        entry_order_response = {
            'status': 'success',
            'message': 'Entry order placed successfully',
            'entry_order_id': order_id,
            'entry_order_status': 'PENDING'
        }
        executor.submit(async_log_order, 'placebracketorder', order_request_data, entry_order_response)

        # Emit entry order confirmation
        socketio.start_background_task(
            socketio.emit,
            'bracket_order_update',
            {
                'symbol': order_data['symbol'],
                'status': 'entry_order_placed',
                'order_id': order_id,
                'message': 'Entry order placed successfully'
            }
        )

        # Step 2: Place GTT OCO orders immediately (positional/overnight orders)
        # This is done in a background thread but starts immediately without waiting
        def place_gtt_orders():
            try:
                # Small delay to ensure entry order is registered in broker's system
                time.sleep(0.5)

                logger.info(f"Attempting to place GTT OCO orders for entry order {order_id}")

                # Prepare GTT OCO order data - using same structure as bracket order
                gtt_order_data = {
                    'symbol': order_data['symbol'],
                    'exchange': order_data['exchange'],
                    'product': order_data['product'],  # NRML for positional/overnight orders
                    'action': order_data['action'].upper(),  # BUY or SELL (entry action)
                    'quantity': order_data['quantity'],
                    'sl_price': float(order_data['sl_price']),
                    'target_price': float(order_data['target_price']),
                    'order_type': 'GTT',
                }

                # Check if broker has GTT order capability
                if hasattr(broker_module, 'place_gtt_order_api'):
                    logger.info(f"Placing GTT OCO orders for {order_data['symbol']} using {broker}")

                    # Call broker's place_gtt_order_api - handles SL and Target together as OCO
                    res_gtt, resp_gtt, order_id_gtt = broker_module.place_gtt_order_api(gtt_order_data, auth_token)

                    if res_gtt and res_gtt.status == 200:
                        logger.info(f"GTT OCO orders placed successfully")

                        # Extract SL and Target order IDs from response (broker-specific)
                        order_id_sl = resp_gtt.get('sl_order_id') or resp_gtt.get('data', {}).get('sl_order_id')
                        order_id_target = resp_gtt.get('target_order_id') or resp_gtt.get('data', {}).get('target_order_id') or order_id_gtt

                        gtt_response = {
                            'status': 'success',
                            'message': 'Bracket order completed successfully',
                            'bracket_order_id': f"{order_id}_GTT",
                            'entry_order_id': order_id,
                            'sl_order_id': order_id_sl,
                            'target_order_id': order_id_target,
                            'gtt_order_id': order_id_gtt
                        }

                        # Log the successful GTT order placement
                        executor.submit(async_log_order, 'placebracketorder', order_request_data, gtt_response)

                        # Emit success notification
                        socketio.start_background_task(
                            socketio.emit,
                            'bracket_order_update',
                            {
                                'symbol': order_data['symbol'],
                                'status': 'completed',
                                'entry_order_id': order_id,
                                'sl_order_id': order_id_sl,
                                'target_order_id': order_id_target,
                                'message': 'Bracket order completed successfully with GTT OCO'
                            }
                        )

                        # Send Telegram alert
                        socketio.start_background_task(
                            telegram_alert_service.send_order_alert,
                            'placebracketorder', order_data, gtt_response, original_data.get('apikey')
                        )
                    else:
                        logger.error(f"GTT OCO order failed: {resp_gtt}")
                        error_msg = resp_gtt.get('message') or resp_gtt.get('data', {}).get('message', 'Failed to place GTT orders')
                        error_resp = {
                            'status': 'partial',
                            'message': f'Entry order placed but GTT OCO order failed: {error_msg}',
                            'entry_order_id': order_id,
                        }
                        executor.submit(async_log_order, 'placebracketorder', order_request_data, error_resp)

                        socketio.start_background_task(
                            socketio.emit,
                            'bracket_order_update',
                            {
                                'symbol': order_data['symbol'],
                                'status': 'partial_failure',
                                'entry_order_id': order_id,
                                'message': f'Entry order placed but GTT OCO order failed: {error_msg}'
                            }
                        )
                else:
                    logger.warning(f"Broker {broker} does not support GTT orders")
                    warning_resp = {
                        'status': 'warning',
                        'message': 'Entry order placed successfully but broker does not support GTT orders for SL and Target',
                        'entry_order_id': order_id,
                    }
                    executor.submit(async_log_order, 'placebracketorder', order_request_data, warning_resp)

                    socketio.start_background_task(
                        socketio.emit,
                        'bracket_order_update',
                        {
                            'symbol': order_data['symbol'],
                            'status': 'partial_completion',
                            'entry_order_id': order_id,
                            'message': 'Only entry order placed - GTT not supported by broker'
                        }
                    )

            except Exception as e:
                logger.exception(f"Error placing GTT orders: {str(e)}")
                error_resp = {
                    'status': 'error',
                    'message': f'Error placing GTT orders: {str(e)}',
                    'entry_order_id': order_id,
                }
                executor.submit(async_log_order, 'placebracketorder', order_request_data, error_resp)

                socketio.start_background_task(
                    socketio.emit,
                    'bracket_order_update',
                    {
                        'symbol': order_data['symbol'],
                        'status': 'error',
                        'entry_order_id': order_id,
                        'message': f'GTT order error: {str(e)}'
                    }
                )

        # Start the background task to place GTT orders immediately
        background_thread = Thread(target=place_gtt_orders)
        background_thread.daemon = True
        background_thread.start()

        # Return success response with entry order details
        response = {
            'status': 'success',
            'message': 'Bracket order initiated - entry order placed, GTT orders pending',
            'entry_order_id': order_id,
            'symbol': order_data['symbol'],
            'entry_price': float(order_data['entry_price']),
            'sl_price': float(order_data['sl_price']),
            'target_price': float(order_data['target_price']),
            'quantity': int(order_data['quantity']),
            'action': order_data['action'].upper()
        }

        # Send Telegram alert
        socketio.start_background_task(
            telegram_alert_service.send_order_alert,
            'placebracketorder', order_data, response, original_data.get('apikey')
        )

        return True, response, 200

    except Exception as e:
        error_msg = f"Error in place_bracket_order_with_auth: {str(e)}"
        logger.exception(error_msg)
        traceback.print_exc()
        error_response = {
            'status': 'error',
            'message': error_msg
        }
        executor.submit(async_log_order, 'placebracketorder', original_data, error_response)
        return False, error_response, 500


def place_bracket_order(
    order_data: Dict[str, Any],
    api_key: str,
    bracket_order_delay: str = "0.5"
) -> Tuple[bool, Dict[str, Any], int]:
    """
    Main function to place a bracket order.

    Args:
        order_data: Order data dictionary
        api_key: API key for authentication
        bracket_order_delay: Delay for order processing (not actively used in current implementation)

    Returns:
        Tuple containing:
        - Success status (bool)
        - Response data (dict)
        - HTTP status code (int)
    """
    try:
        # Get authentication token and broker from API key
        auth_token_result = get_auth_token_broker(api_key)

        if auth_token_result is None or not isinstance(auth_token_result, tuple) or len(auth_token_result) < 2:
            logger.error(f"Invalid authentication for API key: {api_key}")
            error_response = {
                'status': 'error',
                'message': 'Invalid API key or authentication failed'
            }
            return False, error_response, 401

        auth_token, broker = auth_token_result[0], auth_token_result[1]

        if not auth_token or not broker:
            logger.error(f"Authentication token or broker not found for API key: {api_key}")
            error_response = {
                'status': 'error',
                'message': 'Authentication failed'
            }
            return False, error_response, 401

        # Add apikey to original_data for logging
        original_data = copy.deepcopy(order_data)
        original_data['apikey'] = api_key

        # Place the bracket order
        success, response_data, status_code = place_bracket_order_with_auth(
            order_data=order_data,
            auth_token=auth_token,
            broker=broker,
            original_data=original_data
        )

        return success, response_data, status_code

    except Exception as e:
        logger.exception(f"Unexpected error in place_bracket_order: {str(e)}")
        error_response = {
            'status': 'error',
            'message': f'An unexpected error occurred: {str(e)}'
        }
        return False, error_response, 500

