# Bracket Order - Quick Reference Card

## ⚡ Quick Start (60 seconds)

### Option 1: REST API
```bash
curl -X POST http://localhost:5000/api/v1/placebracketorder/ \
  -H "Content-Type: application/json" \
  -d '{
    "apikey": "YOUR_API_KEY",
    "symbol": "INFY",
    "exchange": "NSE",
    "product": "MIS",
    "action": "BUY",
    "quantity": 1,
    "entry_price": 1500,
    "sl_price": 1480,
    "target_price": 1550
  }'
```

### Option 2: TradingView Webhook
Send POST to: `https://yourdomain.com/tradingview/webhook/bracket`

With same JSON payload above.

---

## 📋 Required Fields

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| apikey | string | abc123xyz | Your API key |
| symbol | string | INFY | Trading symbol |
| exchange | string | NSE | NSE, BSE, MCX, NCDEX, FOREX |
| product | string | MIS | MIS, CNC, NRML |
| action | string | BUY | BUY or SELL |
| quantity | integer | 1 | Must be > 0 |
| entry_price | float | 1500.00 | Entry price |
| sl_price | float | 1480.00 | Stop-loss price |
| target_price | float | 1550.00 | Target price |

---

## ✅ Price Validation Rules

### BUY Orders
```
SL < Entry < Target
Example: 1480 < 1500 < 1550 ✓
```

### SELL Orders
```
SL > Entry > Target
Example: 1520 > 1500 > 1480 ✓
```

---

## 🎯 Order Execution Flow

```
Request Received
      ↓
Validate Input
      ↓
Authenticate
      ↓
Place Entry Order ← Returns entry_order_id
      ↓
(Background) Place GTT Orders
├─ SL Order
└─ Target Order
      ↓
Return Response to Client
```

---

## 📊 Response Examples

### Success
```json
{
    "status": "success",
    "entry_order_id": "12345",
    "sl_price": 1480.0,
    "target_price": 1550.0
}
```

### Error
```json
{
    "status": "error",
    "message": "For BUY orders, SL price must be less than entry price"
}
```

---

## 🔧 Configuration

Add to `.env`:
```
BRACKET_ORDER_RATE_LIMIT=2 per second
BRACKET_ORDER_DELAY=0.5
```

---

## 📱 WebSocket Events

Listen for real-time updates:

```javascript
socket.on('bracket_order_update', (data) => {
    console.log(data.status);  // 'entry_order_placed', 'completed', 'error'
    console.log(data.message);
});
```

---

## 🗄️ Database Query

```sql
-- Recent bracket orders
SELECT * FROM order_logs 
WHERE api_type = 'placebracketorder' 
ORDER BY created_at DESC LIMIT 10;

-- Success rate
SELECT COUNT(*),
       SUM(CASE WHEN response_data LIKE '%success%' THEN 1 ELSE 0 END) as success
FROM order_logs 
WHERE api_type = 'placebracketorder';
```

---

## 🐛 Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Invalid exchange | Exchange not in list | Use NSE, BSE, MCX, NCDEX, FOREX |
| SL price must be less | Wrong SL position for BUY | SL < Entry < Target |
| Missing field | Field not provided | Check all required fields |
| Invalid API key | Wrong/expired key | Verify API key in settings |

---

## 💡 Pro Tips

1. **Test First**: Start with quantity=1 in MIS product
2. **Monitor**: Check WebSocket events for real-time updates
3. **Log Queries**: Use order_logs table to track orders
4. **Error Handling**: Always check response.status field
5. **Price Margins**: SL and Target should be reasonable distances from entry

---

## 🔗 Endpoints

| Method | Endpoint | Auth |
|--------|----------|------|
| POST | `/api/v1/placebracketorder/` | API Key (in payload) |
| POST | `/tradingview/webhook/bracket` | None (direct webhook) |

---

## 📝 Optional Fields

```json
{
    "ordertype": "REGULAR",           // Default: REGULAR
    "pricetype": "LIMIT",             // Default: LIMIT
    "disclosed_quantity": 0,          // Default: 0
    "validity": "DAY",                // Default: DAY
    "tag": "my_order_ref"             // Default: ""
}
```

---

## 🚀 Production Checklist

- [ ] Test with your broker
- [ ] Verify GTT order support
- [ ] Check rate limits are sufficient
- [ ] Set up Telegram notifications
- [ ] Monitor WebSocket events
- [ ] Configure database backup
- [ ] Document API key security
- [ ] Test error scenarios
- [ ] Set up order log retention

---

## 📚 Full Documentation

- **BRACKET_ORDER_GUIDE.md** - Complete guide with examples
- **BRACKET_ORDER_EXAMPLES.py** - Code examples in Python/JavaScript
- **BRACKET_ORDER_IMPLEMENTATION.md** - Implementation details

---

## 🎓 Examples

### Python
```python
import requests

response = requests.post(
    'http://localhost:5000/api/v1/placebracketorder/',
    json={
        'apikey': 'key',
        'symbol': 'INFY',
        'exchange': 'NSE',
        'product': 'MIS',
        'action': 'BUY',
        'quantity': 1,
        'entry_price': 1500,
        'sl_price': 1480,
        'target_price': 1550
    }
)
print(response.json())
```

### JavaScript
```javascript
fetch('/api/v1/placebracketorder/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        apikey: 'key',
        symbol: 'INFY',
        exchange: 'NSE',
        product: 'MIS',
        action: 'BUY',
        quantity: 1,
        entry_price: 1500,
        sl_price: 1480,
        target_price: 1550
    })
})
.then(r => r.json())
.then(data => console.log(data.status));
```

### cURL
```bash
curl -X POST http://localhost:5000/api/v1/placebracketorder/ \
  -H "Content-Type: application/json" \
  -d '{"apikey":"key","symbol":"INFY","exchange":"NSE","product":"MIS","action":"BUY","quantity":1,"entry_price":1500,"sl_price":1480,"target_price":1550}'
```

---

## 📞 Support

For issues:
1. Check BRACKET_ORDER_GUIDE.md
2. Review BRACKET_ORDER_EXAMPLES.py
3. Query order_logs table
4. Check WebSocket events
5. Monitor broker API responses

---

**Last Updated**: January 5, 2026  
**Status**: ✓ Production Ready

