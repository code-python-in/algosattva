# TradingView Bracket Order - Quick Reference

## Three Ways to Use TradingView Webhooks

### 1️⃣ Strategy Alert Mode
**When**: Using TradingView strategy templates
**Webhook URL**: `.../api/v1/placesmartorder`
**Fields**: 
- Symbol, Exchange, Product (others are dynamic: `{{strategy.order.action}}`, `{{strategy.order.contracts}}`, etc.)

```json
{
  "apikey": "your_api_key",
  "strategy": "TradingView Strategy",
  "symbol": "INFY",
  "action": "{{strategy.order.action}}",
  "exchange": "NSE",
  "pricetype": "MARKET",
  "product": "MIS",
  "quantity": "{{strategy.order.contracts}}",
  "position_size": "{{strategy.position_size}}"
}
```

---

### 2️⃣ Line Alert Mode
**When**: Drawing trendlines/support/resistance manually
**Webhook URL**: `.../api/v1/placeorder`
**Fields**:
- Symbol, Exchange, Product, Action, Quantity (all static values)

```json
{
  "apikey": "your_api_key",
  "strategy": "TradingView Line Alert",
  "symbol": "INFY",
  "action": "BUY",
  "exchange": "NSE",
  "pricetype": "MARKET",
  "product": "MIS",
  "quantity": "1"
}
```

---

### 3️⃣ **Bracket Order Mode** ⭐ (NEW)
**When**: You want Entry + Stop Loss + Target all placed together
**Webhook URL**: `.../tradingview/webhook/bracket`
**Fields**:
- All static: Symbol, Exchange, Product, Action, Quantity, Entry Price, SL Price, Target Price

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

**What happens:**
1. Entry order placed at 1500.50
2. Stoploss order placed at 1480.00 (SELL)
3. Target order placed at 1520.00 (SELL)
4. When SL executes → Target is cancelled
5. When Target executes → SL is cancelled

---

## UI Walkthrough

### Location
`http://yourdomain.com/tradingview`

### Steps
1. **Select Mode** (top tabs): Strategy Alert | Line Alert | **Bracket Order**
2. **Fill Basic Info** (always visible):
   - Symbol search
   - Exchange dropdown
   - Product type dropdown
3. **Fill Mode-Specific Info**:
   - **Bracket Order**: Action, Quantity, Entry Price, SL Price, Target Price
4. **Generate JSON**: Button auto-generates based on your input
5. **Copy JSON**: Use copy button or select-all + copy
6. **Webhook URL**: Displayed based on selected mode
7. **Copy Webhook URL**: For use in TradingView alert

---

## TradingView Alert Setup

### For Bracket Orders:

1. **Create Alert** in TradingView
   - Right-click any chart → Add Alert
   - Set condition and alert name

2. **Configure Notifications**
   - Click **Notifications** tab
   - Check **Webhook URL**
   - Paste: `https://yourdomain.com/tradingview/webhook/bracket`
   
3. **Add Webhook Message**
   - Paste the JSON from OpenAlgo UI

4. **Create Alert**
   - Click "Create"

---

## Example Scenarios

### Scenario 1: BUY INFY
```json
{
  "apikey": "your_api_key",
  "strategy": "TradingView Bracket Order",
  "symbol": "INFY",
  "exchange": "NSE",
  "product": "MIS",
  "action": "BUY",
  "quantity": "1",
  "entry_price": 1500.00,
  "sl_price": 1485.00,
  "target_price": 1515.00
}
```

**Result**:
- BUY 1 INFY at 1500.00
- SELL 1 INFY at 1485.00 (SL)
- SELL 1 INFY at 1515.00 (Target)
- Whichever executes first, the other is cancelled

---

### Scenario 2: SELL BANKNIFTY
```json
{
  "apikey": "your_api_key",
  "strategy": "TradingView Bracket Order",
  "symbol": "BANKNIFTY",
  "exchange": "NFO",
  "product": "MIS",
  "action": "SELL",
  "quantity": "1",
  "entry_price": 45000.00,
  "sl_price": 45500.00,
  "target_price": 44500.00
}
```

**Result**:
- SELL 1 BANKNIFTY at 45000.00
- BUY 1 BANKNIFTY at 45500.00 (SL - covers loss)
- BUY 1 BANKNIFTY at 44500.00 (Target - takes profit)
- Whichever executes first, the other is cancelled

---

## Webhook Response

**Success (200)**:
```json
{
  "status": "success",
  "bracket_order_id": "550e8400-e29b-41d4-a716-446655440000",
  "entry_order_id": "12345",
  "stoploss_order_id": "12346",
  "target_order_id": "12347",
  "message": "Bracket order placed successfully"
}
```

**Error (400)**:
```json
{
  "status": "error",
  "message": "Missing required fields: entry_price"
}
```

---

## Validation Rules

| Field | Type | Min | Max | Required |
|-------|------|-----|-----|----------|
| apikey | string | 1 | - | ✅ |
| symbol | string | 1 | 20 | ✅ |
| exchange | string | 2 | 10 | ✅ |
| product | string | 2 | 10 | ✅ |
| action | enum | BUY, SELL | - | ✅ |
| quantity | integer | 1 | - | ✅ |
| entry_price | float | 0.01 | - | ✅ |
| sl_price | float | 0.01 | - | ✅ |
| target_price | float | 0.01 | - | ✅ |

---

## Troubleshooting

### Problem: "API key not found"
**Solution**: Configure API key in OpenAlgo UI (Settings → API Keys)

### Problem: "Symbol not found"
**Solution**: Search symbol in UI first to verify it's available, check exchange selection

### Problem: "Missing required fields"
**Solution**: Fill all 9 fields: apikey, symbol, exchange, product, action, quantity, entry_price, sl_price, target_price

### Problem: Webhook URL not showing bracket URL
**Solution**: Make sure you've clicked the "Bracket Order" tab (3rd tab)

### Problem: Orders not executing
**Solution**: 
1. Check broker session is active
2. Verify prices are realistic
3. Confirm quantity is within daily limits
4. Check market is open

---

## Pro Tips

✅ **Test First**: Use Sandbox mode before live trading

✅ **Set Realistic Prices**: Entry should be near current price

✅ **Price Order**: Usually Entry < Target for BUY; Entry > Target for SELL

✅ **SL Distance**: Set SL beyond support/resistance, not too close

✅ **Monitor**: Watch broker's order management for execution

✅ **Alerts**: Set TradingView alerts on confirmed signals only

---

## Related Documentation

- Full Technical Docs: `BRACKET_ORDER_TRADINGVIEW_INTEGRATION.md`
- Bracket Order Service: `services/bracket_order_service.py`
- TradingView Blueprint: `blueprints/tv_json.py`
- UI Template: `templates/tradingview.html`
- JavaScript Logic: `static/js/tradingview.js`

---

**Last Updated**: January 2026
**Supported Brokers**: All brokers supported by OpenAlgo (Zerodha, Angel, DefinedGe, Dhan, etc.)

