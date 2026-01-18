# TradingView Bracket Order Integration

## Overview

The TradingView integration has been enhanced to support **Bracket Order placement** in addition to the existing Strategy Alert and Line Alert modes.

## What Was Added

### 1. **UI Changes** (`templates/tradingview.html`)

#### New Tab
- Added **"Bracket Order"** tab to the mode selector alongside Strategy Alert and Line Alert

#### New Form Fields (visible only in Bracket Order mode)
- **Action**: Select BUY or SELL
- **Quantity**: Number of contracts to trade
- **Entry Price**: Price at which to place the entry order
- **Stoploss Price**: Price at which to trigger the stoploss order
- **Target Price**: Price at which to trigger the target/take-profit order

### 2. **JavaScript Updates** (`static/js/tradingview.js`)

#### New DOM Element References
```javascript
const bracketActionSelect = document.getElementById('bracket-action');
const bracketQuantityInput = document.getElementById('bracket-quantity');
const bracketActionField = document.getElementById('bracket-action-field');
const bracketQuantityField = document.getElementById('bracket-quantity-field');
const entryPriceInput = document.getElementById('entry-price');
const entryPriceField = document.getElementById('entry-price-field');
const slPriceInput = document.getElementById('sl-price');
const slPriceField = document.getElementById('sl-price-field');
const targetPriceInput = document.getElementById('target-price');
const targetPriceField = document.getElementById('target-price-field');
```

#### Enhanced `switchMode()` Function
- Now handles three modes: `strategy`, `line`, and `bracket`
- Shows/hides appropriate form fields based on selected mode
- Updates the webhook URL dynamically:
  - Strategy Alert: `.../api/v1/placesmartorder`
  - Line Alert: `.../api/v1/placeorder`
  - **Bracket Order: `.../tradingview/webhook/bracket`**

#### Updated `generateJSON()` Function
- Extracts bracket order specific data when in bracket mode:
  - `action`: BUY or SELL
  - `quantity`: Number of contracts
  - `entry_price`: Entry order price
  - `sl_price`: Stoploss order price
  - `target_price`: Target/profit order price

#### Event Listeners for Bracket Fields
- Added change listeners to all bracket order input fields
- Automatically regenerates JSON when any field is modified

### 3. **Backend Updates** (`blueprints/tv_json.py`)

#### Enhanced `/tradingview/` Endpoint
Updated the `tradingview_json()` function to handle three modes:

**Bracket Order Mode Processing:**
```python
elif mode == 'bracket':
    # Validates: symbol, exchange, product, action, quantity, entry_price, sl_price, target_price
    # Returns OrderedDict with:
    - apikey
    - strategy: "TradingView Bracket Order"
    - symbol
    - exchange
    - product
    - action
    - quantity
    - entry_price
    - sl_price
    - target_price
```

## How to Use

### 1. **In the UI**
1. Navigate to `/tradingview` endpoint
2. Click the **"Bracket Order"** tab
3. Select Symbol, Exchange, Product
4. Set Action (BUY/SELL) and Quantity
5. Enter Entry Price, Stoploss Price, and Target Price
6. Click "Generate JSON"
7. Copy the generated JSON

### 2. **In TradingView**
1. Create an alert in TradingView
2. Select **Webhook URL** in the alert notification options
3. Use the webhook URL: `https://yourdomain.com/tradingview/webhook/bracket`
4. Paste the generated JSON as the webhook message

### 3. **Example Bracket Order JSON**
```json
{
  "apikey": "your_api_key",
  "strategy": "TradingView Bracket Order",
  "symbol": "INFY",
  "exchange": "NSE",
  "product": "MIS",
  "action": "BUY",
  "quantity": "1",
  "entry_price": 1500.50,
  "sl_price": 1480.00,
  "target_price": 1520.00
}
```

## Webhook Endpoint

### URL
```
POST /tradingview/webhook/bracket
```

### Request Body
```json
{
  "apikey": "string (required)",
  "symbol": "string (required)",
  "exchange": "string (required)",
  "product": "string (required)",
  "action": "BUY|SELL (required)",
  "quantity": "integer (required)",
  "entry_price": "float (required)",
  "sl_price": "float (required)",
  "target_price": "float (required)"
}
```

### Response
```json
{
  "status": "success",
  "bracket_order_id": "uuid",
  "entry_order_id": "order_id",
  "stoploss_order_id": "order_id",
  "target_order_id": "order_id",
  "message": "Bracket order placed successfully"
}
```

## One-Cancels-Other (OCO) Logic

The bracket order placement automatically implements **One-Cancels-Other** logic:

1. **Entry Order**: Places the main entry order at the specified `entry_price`
2. **Stoploss Order**: Places a stoploss order (opposite direction) at `sl_price`
3. **Target Order**: Places a target/profit order (opposite direction) at `target_price`

When the entry order executes:
- Waits for either stoploss or target to execute
- When one executes, automatically cancels the other

## Configuration Files Modified

| File | Changes |
|------|---------|
| `templates/tradingview.html` | Added Bracket Order tab and form fields |
| `static/js/tradingview.js` | Added bracket order mode handling, event listeners, and JSON generation |
| `blueprints/tv_json.py` | Added bracket order mode processing in `/tradingview/` endpoint |

## Backward Compatibility

✅ **Fully backward compatible**
- Existing Strategy Alert and Line Alert modes work exactly as before
- New Bracket Order mode is additive and doesn't affect existing functionality
- All three modes are now available in the TradingView configuration page

## Testing

To test the Bracket Order functionality:

1. Go to `/tradingview` endpoint
2. Click the **Bracket Order** tab
3. Fill in all required fields with test data
4. Click "Generate JSON"
5. Verify the webhook URL shows: `.../tradingview/webhook/bracket`
6. Verify the JSON output contains all bracket order fields

## Related Services

The bracket order webhook uses the existing `bracket_order_service.place_bracket_order()` function, which:
- Validates the API key
- Places three orders (entry, SL, target) with proper linking
- Implements one-cancels-other cancellation logic
- Tracks order execution and cancels opposing legs as needed

## Future Enhancements

Possible improvements:
- Support for trailing stoploss
- Support for quantity fractioning based on entry fills
- Support for breakeven orders
- WebSocket-based real-time bracket order management
- Dashboard to monitor active bracket orders from TradingView

