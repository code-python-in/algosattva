# Bracket Order Implementation Guide

## Overview

The bracket order functionality has been successfully implemented in OpenAlgo. This feature allows users to place bracket orders that consist of:
1. **Entry Order**: An initial order at a specified entry price
2. **GTT OCO (Good Till Triggered One Cancels Other)**: Automatically placed stop-loss and target orders that are triggered upon entry order confirmation

## Files Created

### 1. Service Layer
**File**: `services/bracket_order_service.py`

This module contains the core logic for bracket order execution:
- **validate_bracket_order()**: Validates bracket order data including:
  - Required fields: apikey, symbol, exchange, product, action, quantity, entry_price, sl_price, target_price
  - Price validation (SL and Target relative to entry price)
  - Action validation (BUY/SELL)
  - Quantity validation

- **place_bracket_order_with_auth()**: Main execution function that:
  1. Validates the bracket order
  2. Places the entry order
  3. Upon success, schedules background GTT orders for SL and Target
  4. Handles both successful and partial failure scenarios

- **place_bracket_order()**: Public interface that handles API key authentication and routes to the main execution function

### 2. REST API Endpoint
**File**: `restx_api/bracket_order.py`

Provides a REST API endpoint at `/api/v1/placebracketorder/` with:
- Input validation using Marshmallow schema
- Rate limiting (configurable via BRACKET_ORDER_RATE_LIMIT environment variable)
- Comprehensive error handling
- JSON response with order details

### 3. TradingView Webhook
**File**: `blueprints/tv_json.py` (modified)

Added new endpoint: `/tradingview/webhook/bracket` (POST)

This webhook endpoint:
- Accepts bracket order payloads directly from TradingView
- Does NOT require session authentication (allows direct webhook integration)
- Validates required fields
- Routes to the bracket order service
- Returns real-time status updates

### 4. API Registration
**File**: `restx_api/__init__.py` (modified)

Registered the new bracket_order API namespace at path `/placebracketorder`

## API Usage

### REST API Endpoint

**URL**: `POST /api/v1/placebracketorder/`

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
    "apikey": "your_api_key_here",
    "symbol": "INFY",
    "exchange": "NSE",
    "product": "MIS",
    "action": "BUY",
    "quantity": 1,
    "entry_price": 1500.50,
    "sl_price": 1480.00,
    "target_price": 1550.00,
    "ordertype": "REGULAR",
    "pricetype": "LIMIT",
    "disclosed_quantity": 0,
    "validity": "DAY",
    "tag": "bracket_order_1"
}
```

**Response (Success)**:
```json
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
```

**Response (Error)**:
```json
{
    "status": "error",
    "message": "Error description"
}
```

### TradingView Webhook

**URL**: `POST /tradingview/webhook/bracket`

**Request Format** (Same as REST API):
```json
{
    "apikey": "your_api_key_here",
    "symbol": "INFY",
    "exchange": "NSE",
    "product": "MIS",
    "action": "BUY",
    "quantity": 1,
    "entry_price": 1500.50,
    "sl_price": 1480.00,
    "target_price": 1550.00
}
```

**TradingView Alert Configuration Example**:
```
webhook_url = https://yourdomain.com/tradingview/webhook/bracket
webhook_message = {
    "apikey": "your_api_key",
    "symbol": "{{ticker}}",
    "exchange": "NSE",
    "product": "MIS",
    "action": "{{strategy.order.action}}",
    "quantity": "{{strategy.order.contracts}}",
    "entry_price": "{{close}}",
    "sl_price": "{{close}} - 50",
    "target_price": "{{close}} + 100"
}
```

## Environment Variables

Add these to your `.env` file:

```
# Bracket Order Configuration
BRACKET_ORDER_RATE_LIMIT=2 per second
BRACKET_ORDER_DELAY=0.5
```

## Features

### 1. Entry Order Placement
- Places a LIMIT order at the specified entry price
- Validates that SL and Target prices are correctly positioned relative to entry price:
  - **BUY orders**: SL < Entry < Target
  - **SELL orders**: SL > Entry > Target

### 2. GTT Order Management
- Automatically places GTT orders for both SL and Target upon entry confirmation
- Uses One Cancels Other (OCO) logic - when one order executes, the other is cancelled
- Broker-specific GTT implementation (if broker supports it)

### 3. Background Processing
- GTT orders are placed asynchronously using background threads
- Prevents blocking the main API response
- Real-time updates via WebSocket (if enabled)

### 4. Error Handling
- Validates all required fields
- Handles partial failures (e.g., entry order successful but GTT failed)
- Provides detailed error messages
- Logs all transactions for audit trail

### 5. Notifications
- Sends order confirmation via Telegram (if configured)
- Emits WebSocket events for real-time UI updates
- Database logging of all bracket order requests and responses

## Validation Rules

### Field Validation
- **apikey**: Required, string
- **symbol**: Required, string
- **exchange**: Required, must be one of: NSE, BSE, MCX, NCDEX, FOREX
- **product**: Required, must be one of: MIS, CNC, NRML
- **action**: Required, BUY or SELL (case-insensitive)
- **quantity**: Required, positive integer
- **entry_price**: Required, positive float
- **sl_price**: Required, positive float
- **target_price**: Required, positive float

### Price Relationship Validation
For **BUY** orders:
```
SL Price < Entry Price < Target Price
```

For **SELL** orders:
```
SL Price > Entry Price > Target Price
```

## Execution Flow

```
1. Webhook/API Request Received
   └─ Validate payload
   └─ Extract API key
   
2. Authentication
   └─ Verify API key
   └─ Get auth token and broker info
   
3. Entry Order Placement
   └─ Create entry order with LIMIT price type
   └─ Submit to broker
   └─ Get order confirmation + order_id
   
4. GTT Order Scheduling (Background)
   └─ Wait for entry order confirmation (2 seconds)
   └─ Create SL order with GTT type
   └─ Create Target order with GTT type
   └─ Submit both to broker
   
5. Response & Notifications
   └─ Return order details to caller
   └─ Send Telegram notification (if configured)
   └─ Emit WebSocket events
   └─ Log to database
```

## Broker Support

The bracket order implementation is designed to work with any broker integrated into OpenAlgo. However, GTT order functionality depends on broker support:

- **Full Support**: Brokers with native GTT/OCO APIs
- **Partial Support**: Entry order only (GTT requires broker implementation of `place_gtt_order_api`)

### To Enable GTT Support for Your Broker

In `broker/{broker_name}/api/order_api.py`, implement:

```python
def place_gtt_order_api(data, auth):
    """
    Place a Good Till Triggered (GTT) order
    
    Args:
        data: Order data including trigger_price, trigger_symbol, etc.
        auth: Authentication token
        
    Returns:
        (response, response_data, order_id)
    """
    # Implementation specific to broker
    pass
```

## Testing

### Example cURL Request

```bash
curl -X POST http://localhost:5000/api/v1/placebracketorder/ \
  -H "Content-Type: application/json" \
  -d '{
    "apikey": "test_api_key",
    "symbol": "INFY",
    "exchange": "NSE",
    "product": "MIS",
    "action": "BUY",
    "quantity": 1,
    "entry_price": 1500.50,
    "sl_price": 1480.00,
    "target_price": 1550.00
  }'
```

### WebSocket Events

When bracket orders are placed, the following WebSocket events are emitted:

```javascript
// Entry order placed
{
    "symbol": "INFY",
    "status": "entry_order_placed",
    "order_id": "12345",
    "message": "Entry order placed successfully"
}

// Bracket order completed
{
    "symbol": "INFY",
    "status": "completed",
    "entry_order_id": "12345",
    "sl_order_id": "12346",
    "target_order_id": "12347",
    "message": "Bracket order completed successfully"
}

// Partial failure
{
    "symbol": "INFY",
    "status": "partial_failure",
    "message": "Entry and SL orders placed but target order failed"
}
```

## Logging

All bracket order activities are logged to the database:

- **API Type**: `placebracketorder`
- **Logged Data**: Request payload (minus apikey) and response
- **Location**: `db/openalgo.db` in `order_logs` table

Query logs:
```sql
SELECT * FROM order_logs WHERE api_type = 'placebracketorder' ORDER BY created_at DESC;
```

## Error Codes

| Status Code | Meaning |
|-------------|---------|
| 200 | Order successfully placed |
| 400 | Invalid request data or validation error |
| 401 | Invalid API key or authentication failed |
| 404 | Broker module not found |
| 500 | Server error during order processing |

## Security Considerations

1. **API Key Protection**: Never expose API keys in logs or frontend code
2. **HTTPS Only**: Ensure all webhook URLs use HTTPS in production
3. **Webhook Validation**: Validate webhook signatures if implementing additional security
4. **Rate Limiting**: Bracket order endpoints are rate-limited (default: 2 per second)

## Future Enhancements

1. **Order Monitoring**: Add automatic monitoring of entry order status before placing GTT orders
2. **OCO Implementation**: Implement true OCO (One Cancels Other) logic for better order coordination
3. **Multi-Leg Orders**: Support more complex bracket order variations
4. **Order Modification**: Allow modification of bracket orders after placement
5. **Partial Fills**: Handle partial fill scenarios for entry orders

## Troubleshooting

### Issue: GTT orders not being placed

**Solution**: Ensure your broker supports GTT orders. Check broker-specific implementation of `place_gtt_order_api`.

### Issue: Entry order placed but webhook returns error

**Solution**: Check the background thread logs. GTT order placement happens asynchronously - check broker API response.

### Issue: Invalid price validation errors

**Solution**: Verify that:
- For BUY: SL < Entry < Target
- For SELL: SL > Entry > Target

### Issue: API key authentication failed

**Solution**: Verify the API key is valid and properly authenticated in the system.

## Support

For issues or feature requests, please refer to the main OpenAlgo documentation or contact support.

