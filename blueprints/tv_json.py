# blueprints/tv_json.py

from flask import Blueprint, render_template, request, jsonify, session, url_for, redirect
from database.symbol import enhanced_search_symbols
from database.auth_db import get_api_key_for_tradingview
from utils.session import check_session_validity
from collections import OrderedDict
from services.bracket_order_service import place_bracket_order
import os
import logging

logger = logging.getLogger(__name__)

host = os.getenv('HOST_SERVER')

tv_json_bp = Blueprint('tv_json_bp', __name__, url_prefix='/tradingview')

@tv_json_bp.route('/', methods=['GET', 'POST'])
@check_session_validity
def tradingview_json():
    if request.method == 'POST':
        try:
            symbol_input = request.json.get('symbol')
            exchange = request.json.get('exchange')
            product = request.json.get('product')
            mode = request.json.get('mode', 'strategy')  # 'strategy', 'line', or 'bracket'

            # Get actual API key for TradingView
            api_key = get_api_key_for_tradingview(session.get('user'))
            broker = session.get('broker')

            if not api_key:
                logger.error(f"API key not found for user: {session.get('user')}")
                return jsonify({'error': 'API key not found'}), 404

            # Use enhanced search function
            if symbol_input == "{{ticker}}":
                symbols = enhanced_search_symbols("SAIL", exchange)
            else:
                symbols = enhanced_search_symbols(symbol_input, exchange)
            if not symbols:
                logger.warning(f"Symbol not found: {symbol_input}")
                return jsonify({'error': 'Symbol not found'}), 404

            symbol_data = symbols[0]  # Take the first match
            logger.info(f"Found matching symbol: {symbol_data.symbol}")

            if mode == 'line':
                # Line Alert Mode - similar to GoCharting (uses placeorder)
                action = request.json.get('action')
                quantity = request.json.get('quantity')

                if not all([symbol_input, exchange, product, action, quantity]):
                    logger.error("Missing required fields in TradingView Line Alert request")
                    return jsonify({'error': 'Missing required fields'}), 400

                logger.info(f"Processing TradingView Line Alert - Symbol: {symbol_input}, Action: {action}, Quantity: {quantity}")

                json_data = OrderedDict([
                    ("apikey", api_key),
                    ("strategy", "TradingView Line Alert"),
                    ("symbol", symbol_data.symbol),
                    ("action", action.upper()),
                    ("exchange", symbol_data.exchange),
                    ("pricetype", "MARKET"),
                    ("product", product),
                    ("quantity", str(quantity)),
                ])
            elif mode == 'bracket':
                # Bracket Order Mode
                action = request.json.get('action')
                quantity = request.json.get('quantity')
                entry_price = request.json.get('entry_price')
                sl_price = request.json.get('sl_price')
                target_price = request.json.get('target_price')

                if not all([symbol_input, exchange, product, action, quantity, entry_price, sl_price, target_price]):
                    logger.error("Missing required fields in TradingView Bracket Order request")
                    return jsonify({'error': 'Missing required fields'}), 400

                logger.info(f"Processing TradingView Bracket Order - Symbol: {symbol_input}, Action: {action}, Quantity: {quantity}, Entry: {entry_price}, SL: {sl_price}, Target: {target_price}")

                json_data = OrderedDict([
                    ("apikey", api_key),
                    ("strategy", "TradingView Bracket Order"),
                    ("symbol", "{{ticker}}"),
                    ("exchange", symbol_data.exchange),
                    ("product", product),
                    ("action", action.upper()),
                    ("quantity", str(quantity)),
                    ("entry_price", float(entry_price)),
                    ("sl_price", float(sl_price)),
                    ("target_price", float(target_price)),
                ])
            else:
                # Strategy Alert Mode - original behavior (uses placesmartorder)
                if not all([symbol_input, exchange, product]):
                    logger.error("Missing required fields in TradingView Strategy request")
                    return jsonify({'error': 'Missing required fields'}), 400

                logger.info(f"Processing TradingView Strategy Alert - Symbol: {symbol_input}, Exchange: {exchange}, Product: {product}")

                json_data = OrderedDict([
                    ("apikey", api_key),
                    ("strategy", "TradingView Strategy"),
                    ("symbol", symbol_data.symbol),
                    ("action", "{{strategy.order.action}}"),
                    ("exchange", symbol_data.exchange),
                    ("pricetype", "MARKET"),
                    ("product", product),
                    ("quantity", "{{strategy.order.contracts}}"),
                    ("position_size", "{{strategy.position_size}}"),
                ])

            logger.info("Successfully generated TradingView webhook data")
            return jsonify(json_data)

        except Exception as e:
            logger.error(f"Error processing TradingView request: {str(e)}")
            return jsonify({'error': str(e)}), 500

    return render_template('tradingview.html', host=host)


@tv_json_bp.route('/webhook/bracket', methods=['POST'])
def tradingview_bracket_webhook():
    """
    TradingView Webhook for Bracket Orders

    Expected JSON payload from TradingView:
    {
        "apikey": "your_api_key",
        "symbol": "INFY",
        "exchange": "NSE",
        "product": "MIS",
        "action": "BUY",
        "quantity": 1,
        "entry_price": 1500.50,
        "sl_price": 1480.00,
        "target_price": 1550.00
    }

    This endpoint processes bracket orders without requiring session authentication,
    allowing for direct webhook calls from TradingView.
    """
    try:
        if not request.json:
            logger.error("No JSON payload provided in TradingView bracket webhook")
            return jsonify({'status': 'error', 'message': 'No JSON payload provided'}), 400

        payload = request.json

        # Validate required fields
        required_fields = ['apikey', 'symbol', 'exchange', 'product', 'action', 'quantity', 'entry_price', 'sl_price', 'target_price']
        missing_fields = [field for field in required_fields if field not in payload]

        if missing_fields:
            error_msg = f'Missing required fields: {", ".join(missing_fields)}'
            logger.error(f"TradingView bracket webhook missing fields: {error_msg}")
            return jsonify({'status': 'error', 'message': error_msg}), 400

        logger.info(f"Processing TradingView bracket order webhook - Symbol: {payload.get('symbol')}, Action: {payload.get('action')}")

        # Extract API key
        api_key = payload.pop('apikey', None)

        # Call the bracket order service
        success, response_data, status_code = place_bracket_order(
            order_data=payload,
            api_key=api_key
        )

        logger.info(f"TradingView bracket webhook processed with status: {response_data.get('status')}")
        return jsonify(response_data), status_code

    except Exception as e:
        logger.error(f"Error processing TradingView bracket webhook: {str(e)}")
        error_response = {
            'status': 'error',
            'message': f'Error processing bracket order: {str(e)}'
        }
        return jsonify(error_response), 500

