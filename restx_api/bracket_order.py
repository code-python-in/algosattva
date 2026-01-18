from flask_restx import Namespace, Resource
from flask import request, jsonify, make_response
from marshmallow import ValidationError, Schema, fields
from limiter import limiter
import os

from services.bracket_order_service import place_bracket_order
from database.apilog_db import async_log_order, executor
from utils.logging import get_logger

BRACKET_ORDER_RATE_LIMIT = os.getenv("BRACKET_ORDER_RATE_LIMIT", "2 per second")
BRACKET_ORDER_DELAY = os.getenv("BRACKET_ORDER_DELAY", "0.5")

api = Namespace('bracket_order', description='Place Bracket Order API')

# Initialize logger
logger = get_logger(__name__)


class BracketOrderSchema(Schema):
    """Schema for validating bracket order requests"""
    apikey = fields.String(required=True, description='API Key')
    symbol = fields.String(required=True, description='Trading Symbol')
    exchange = fields.String(required=True, description='Exchange (NSE, BSE, MCX, NCDEX, FOREX)')
    product = fields.String(required=True, description='Product Type (MIS, CNC, NRML)')
    action = fields.String(required=True, description='Order Action (BUY or SELL)')
    quantity = fields.Integer(required=True, description='Order Quantity')
    entry_price = fields.Float(required=True, description='Entry Price')
    sl_price = fields.Float(required=True, description='Stop Loss Price')
    target_price = fields.Float(required=True, description='Target Price')
    ordertype = fields.String(missing='REGULAR', description='Order Type (REGULAR, BO)')
    pricetype = fields.String(missing='LIMIT', description='Price Type (LIMIT, MARKET, SL, SL-M)')
    disclosed_quantity = fields.Integer(missing=0, description='Disclosed Quantity')
    validity = fields.String(missing='DAY', description='Order Validity (DAY, IOC, FOK)')
    tag = fields.String(missing='', description='Order Tag/Reference')


# Initialize schema
bracket_order_schema = BracketOrderSchema()


@api.route('/', strict_slashes=False)
class BracketOrder(Resource):
    @limiter.limit(BRACKET_ORDER_RATE_LIMIT)
    def post(self):
        """
        Place a bracket order with entry order and GTT OCO (One Cancels Other) for SL and Target

        Expected JSON payload:
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

        Returns:
        {
            "status": "success",
            "message": "Bracket order initiated - entry order placed, GTT orders pending",
            "entry_order_id": "12345",
            "symbol": "INFY",
            "entry_price": 1500.50,
            "sl_price": 1480.00,
            "target_price": 1550.00,
            "quantity": 1,
            "action": "BUY"
        }
        """
        try:
            data = request.json

            # Validate and deserialize input
            try:
                order_data = bracket_order_schema.load(data)
            except ValidationError as err:
                error_message = str(err.messages)
                logger.warning(f"Validation error in bracket order: {error_message}")
                error_response = {'status': 'error', 'message': error_message}
                executor.submit(async_log_order, 'placebracketorder', data, error_response)
                return make_response(jsonify(error_response), 400)

            # Extract API key
            api_key = order_data.pop('apikey', None)

            # Call the service function to place the bracket order
            success, response_data, status_code = place_bracket_order(
                order_data=order_data,
                api_key=api_key,
                bracket_order_delay=BRACKET_ORDER_DELAY
            )

            return make_response(jsonify(response_data), status_code)

        except Exception as e:
            logger.exception("An unexpected error occurred in BracketOrder endpoint.")
            error_message = 'An unexpected error occurred'
            data = request.json if request.json else {}
            error_response = {'status': 'error', 'message': error_message}
            executor.submit(async_log_order, 'placebracketorder', data, error_response)
            return make_response(jsonify(error_response), 500)
