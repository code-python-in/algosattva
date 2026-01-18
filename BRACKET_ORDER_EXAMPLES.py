"""
Bracket Order Examples and Test Cases

This file contains practical examples and test cases for the bracket order implementation.
"""

# ============================================================================
# EXAMPLE 1: REST API - Simple BUY Bracket Order
# ============================================================================

# cURL Command
EXAMPLE_1_CURL = """
curl -X POST http://localhost:5000/api/v1/placebracketorder/ \
  -H "Content-Type: application/json" \
  -d '{
    "apikey": "your_api_key_here",
    "symbol": "INFY",
    "exchange": "NSE",
    "product": "MIS",
    "action": "BUY",
    "quantity": 1,
    "entry_price": 1500.00,
    "sl_price": 1480.00,
    "target_price": 1550.00
  }'
"""

# Python Example
EXAMPLE_1_PYTHON = """
import requests

api_endpoint = "http://localhost:5000/api/v1/placebracketorder/"

payload = {
    "apikey": "your_api_key_here",
    "symbol": "INFY",
    "exchange": "NSE",
    "product": "MIS",
    "action": "BUY",
    "quantity": 1,
    "entry_price": 1500.00,
    "sl_price": 1480.00,
    "target_price": 1550.00
}

response = requests.post(api_endpoint, json=payload)
print(response.json())
"""

# Expected Response
EXAMPLE_1_RESPONSE = """
{
    "status": "success",
    "message": "Bracket order initiated - entry order placed, GTT orders pending",
    "entry_order_id": "101234567",
    "symbol": "INFY",
    "entry_price": 1500.0,
    "sl_price": 1480.0,
    "target_price": 1550.0,
    "quantity": 1,
    "action": "BUY"
}
"""

# ============================================================================
# EXAMPLE 2: REST API - SELL Bracket Order with Optional Fields
# ============================================================================

EXAMPLE_2_PYTHON = """
import requests

api_endpoint = "http://localhost:5000/api/v1/placebracketorder/"

payload = {
    "apikey": "your_api_key_here",
    "symbol": "TCS",
    "exchange": "NSE",
    "product": "NRML",  # Delivery product
    "action": "SELL",
    "quantity": 2,
    "entry_price": 3500.00,
    "sl_price": 3550.00,     # Note: For SELL, SL > Entry
    "target_price": 3450.00,  # Note: For SELL, Target < Entry
    "ordertype": "REGULAR",
    "pricetype": "LIMIT",
    "disclosed_quantity": 0,
    "validity": "DAY",
    "tag": "tech_sell_1"
}

response = requests.post(api_endpoint, json=payload)
result = response.json()

if result["status"] == "success":
    print(f"Entry Order ID: {result['entry_order_id']}")
    print(f"Symbol: {result['symbol']}")
    print(f"Quantity: {result['quantity']}")
else:
    print(f"Error: {result['message']}")
"""

# ============================================================================
# EXAMPLE 3: TradingView Webhook Configuration
# ============================================================================

EXAMPLE_3_TRADINGVIEW_WEBHOOK = """
# TradingView Pine Script Alert Configuration

# Webhook URL (no session required)
https://yourdomain.com/tradingview/webhook/bracket

# Webhook Message (JSON format)
{
    "apikey": "your_api_key",
    "symbol": "{{ticker}}",
    "exchange": "NSE",
    "product": "MIS",
    "action": "{{strategy.order.action}}",
    "quantity": "{{strategy.order.contracts}}",
    "entry_price": "{{close}}",
    "sl_price": "{{close}} * 0.99",
    "target_price": "{{close}} * 1.02"
}

# Example with fixed prices (for testing)
{
    "apikey": "your_api_key",
    "symbol": "RELIANCE",
    "exchange": "NSE",
    "product": "MIS",
    "action": "BUY",
    "quantity": "1",
    "entry_price": "2500.00",
    "sl_price": "2480.00",
    "target_price": "2550.00"
}
"""

# ============================================================================
# EXAMPLE 4: JavaScript Fetch API
# ============================================================================

EXAMPLE_4_JAVASCRIPT = """
async function placeBracketOrder() {
    const payload = {
        apikey: "your_api_key_here",
        symbol: "HDFC",
        exchange: "NSE",
        product: "MIS",
        action: "BUY",
        quantity: 1,
        entry_price: 2800.00,
        sl_price: 2750.00,
        target_price: 2850.00
    };

    try {
        const response = await fetch('/api/v1/placebracketorder/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        
        if (result.status === 'success') {
            console.log('Bracket order placed successfully!');
            console.log('Entry Order ID:', result.entry_order_id);
            console.log('Symbol:', result.symbol);
            console.log('Entry Price:', result.entry_price);
            console.log('SL Price:', result.sl_price);
            console.log('Target Price:', result.target_price);
        } else {
            console.error('Error:', result.message);
        }
    } catch (error) {
        console.error('Request failed:', error);
    }
}

// Listen for bracket order updates via WebSocket
function setupBracketOrderListener() {
    const socket = io();
    
    socket.on('bracket_order_update', (data) => {
        console.log('Bracket Order Update:', data);
        
        switch(data.status) {
            case 'entry_order_placed':
                console.log(`Entry order placed: ${data.order_id}`);
                break;
            case 'completed':
                console.log(`Bracket order completed!`);
                console.log(`SL Order: ${data.sl_order_id}`);
                console.log(`Target Order: ${data.target_order_id}`);
                break;
            case 'partial_failure':
                console.warn(`Partial failure: ${data.message}`);
                break;
            case 'error':
                console.error(`Error: ${data.message}`);
                break;
        }
    });
}
"""

# ============================================================================
# EXAMPLE 5: Error Handling Examples
# ============================================================================

EXAMPLE_5_ERROR_CASES = """
# Error Case 1: Missing Required Field
Request:
{
    "apikey": "your_api_key",
    "symbol": "INFY",
    "exchange": "NSE",
    "product": "MIS",
    "action": "BUY",
    "quantity": 1,
    "entry_price": 1500.00
    # Missing: sl_price and target_price
}

Response (400):
{
    "status": "error",
    "message": "Missing mandatory field(s): sl_price, target_price"
}

---

# Error Case 2: Invalid Price Relationship (BUY order)
Request:
{
    "apikey": "your_api_key",
    "symbol": "INFY",
    "exchange": "NSE",
    "product": "MIS",
    "action": "BUY",
    "quantity": 1,
    "entry_price": 1500.00,
    "sl_price": 1550.00,  # WRONG: SL should be < Entry for BUY
    "target_price": 1600.00
}

Response (400):
{
    "status": "error",
    "message": "For BUY orders, SL price must be less than entry price"
}

---

# Error Case 3: Invalid API Key
Request:
{
    "apikey": "invalid_key",
    "symbol": "INFY",
    "exchange": "NSE",
    "product": "MIS",
    "action": "BUY",
    "quantity": 1,
    "entry_price": 1500.00,
    "sl_price": 1480.00,
    "target_price": 1550.00
}

Response (401):
{
    "status": "error",
    "message": "Invalid API key or authentication failed"
}

---

# Error Case 4: Invalid Exchange
Request:
{
    "apikey": "your_api_key",
    "symbol": "INFY",
    "exchange": "INVALID",  # Not in [NSE, BSE, MCX, NCDEX, FOREX]
    "product": "MIS",
    "action": "BUY",
    "quantity": 1,
    "entry_price": 1500.00,
    "sl_price": 1480.00,
    "target_price": 1550.00
}

Response (400):
{
    "status": "error",
    "message": "Invalid exchange. Must be one of: NSE, BSE, MCX, NCDEX, FOREX"
}

---

# Error Case 5: Invalid Quantity
Request:
{
    "apikey": "your_api_key",
    "symbol": "INFY",
    "exchange": "NSE",
    "product": "MIS",
    "action": "BUY",
    "quantity": 0,  # Must be > 0
    "entry_price": 1500.00,
    "sl_price": 1480.00,
    "target_price": 1550.00
}

Response (400):
{
    "status": "error",
    "message": "Quantity must be greater than 0"
}

---

# Error Case 6: Partial Success (Entry OK, GTT Failed)
Response (200):
{
    "status": "success",
    "message": "Bracket order initiated - entry order placed, GTT orders pending",
    "entry_order_id": "101234567",
    "symbol": "INFY",
    "entry_price": 1500.0,
    "sl_price": 1480.0,
    "target_price": 1550.0,
    "quantity": 1,
    "action": "BUY"
}

# But WebSocket event shows partial failure:
{
    "symbol": "INFY",
    "status": "partial_failure",
    "message": "Entry and SL orders placed but target order failed"
}
"""

# ============================================================================
# EXAMPLE 6: Different Order Types
# ============================================================================

EXAMPLE_6_ORDER_TYPES = """
# Example 1: Intraday (MIS) - Small Quantities
{
    "apikey": "your_api_key",
    "symbol": "SBIN",
    "exchange": "NSE",
    "product": "MIS",
    "action": "BUY",
    "quantity": 5,
    "entry_price": 500.00,
    "sl_price": 495.00,
    "target_price": 510.00
}

---

# Example 2: Delivery (CNC) - Larger Orders
{
    "apikey": "your_api_key",
    "symbol": "LT",
    "exchange": "NSE",
    "product": "CNC",
    "action": "BUY",
    "quantity": 10,
    "entry_price": 1800.00,
    "sl_price": 1750.00,
    "target_price": 1900.00
}

---

# Example 3: Normal (NRML) - Margin Product
{
    "apikey": "your_api_key",
    "symbol": "BAJAJFINSV",
    "exchange": "NSE",
    "product": "NRML",
    "action": "SELL",
    "quantity": 1,
    "entry_price": 1200.00,
    "sl_price": 1250.00,
    "target_price": 1150.00
}

---

# Example 4: MCX Commodity (Gold)
{
    "apikey": "your_api_key",
    "symbol": "GOLDPETAL",
    "exchange": "MCX",
    "product": "NRML",
    "action": "BUY",
    "quantity": 1,
    "entry_price": 68000.00,
    "sl_price": 67500.00,
    "target_price": 68500.00
}
"""

# ============================================================================
# EXAMPLE 7: Monitoring Bracket Orders
# ============================================================================

EXAMPLE_7_MONITORING = """
# Query database for recent bracket orders
SELECT * FROM order_logs 
WHERE api_type = 'placebracketorder' 
ORDER BY created_at DESC 
LIMIT 10;

# Check specific bracket order
SELECT request_data, response_data, created_at 
FROM order_logs 
WHERE api_type = 'placebracketorder' 
  AND response_data LIKE '%INFY%'
ORDER BY created_at DESC;

# Get success count
SELECT COUNT(*) as total, 
       SUM(CASE WHEN response_data LIKE '%success%' THEN 1 ELSE 0 END) as successful
FROM order_logs 
WHERE api_type = 'placebracketorder';
"""

# ============================================================================
# EXAMPLE 8: Production Checklist
# ============================================================================

EXAMPLE_8_PRODUCTION_CHECKLIST = """
Before deploying bracket orders to production:

[ ] 1. Set environment variables in .env:
    - BRACKET_ORDER_RATE_LIMIT=2 per second
    - BRACKET_ORDER_DELAY=0.5

[ ] 2. Verify broker support:
    - Check if broker has place_gtt_order_api implementation
    - Test GTT order placement in broker's sandbox

[ ] 3. Test with small quantities:
    - Start with quantity=1
    - Verify entry order placement
    - Check GTT order creation

[ ] 4. Validate price relationships:
    - Test BUY orders (SL < Entry < Target)
    - Test SELL orders (SL > Entry > Target)
    - Confirm validation works for edge cases

[ ] 5. Set up monitoring:
    - Configure Telegram alerts (if using)
    - Enable WebSocket event logging
    - Monitor database for order logs

[ ] 6. Security checks:
    - Ensure API keys are secure
    - Use HTTPS for webhook URLs
    - Validate webhook payloads

[ ] 7. Performance testing:
    - Test concurrent bracket orders
    - Monitor rate limiting
    - Check background thread performance

[ ] 8. Documentation:
    - Update API documentation
    - Provide webhook configuration examples
    - Document error codes and recovery steps

[ ] 9. Backup and recovery:
    - Test database backup procedures
    - Verify order log retention
    - Plan for system failures

[ ] 10. User training:
    - Train support team on bracket orders
    - Document FAQ and troubleshooting
    - Create user guides with examples
"""

if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*80)
    print("EXAMPLES AVAILABLE:")
    print("="*80)
    print("EXAMPLE_1_CURL - Simple REST API cURL command")
    print("EXAMPLE_1_PYTHON - Simple REST API Python example")
    print("EXAMPLE_1_RESPONSE - Expected API response")
    print("EXAMPLE_2_PYTHON - SELL order with optional fields")
    print("EXAMPLE_3_TRADINGVIEW_WEBHOOK - TradingView webhook setup")
    print("EXAMPLE_4_JAVASCRIPT - JavaScript Fetch API example")
    print("EXAMPLE_5_ERROR_CASES - Error handling examples")
    print("EXAMPLE_6_ORDER_TYPES - Different order type examples")
    print("EXAMPLE_7_MONITORING - Database query examples")
    print("EXAMPLE_8_PRODUCTION_CHECKLIST - Production deployment checklist")

