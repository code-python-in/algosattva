# Bracket Order - Integration Points & Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Client Applications                         │
├──────────────────────┬──────────────────────┬───────────────────┤
│   REST API Client    │   TradingView Alert  │   WebSocket Events │
│  (Python/Node/etc)   │   Webhook            │   (Real-time UI)   │
└──────────────────────┴──────────────────────┴───────────────────┘
         │                      │                      │
         │                      │                      │
    POST /api/v1/            POST /tradingview/    Listen to
    placebracketorder/       webhook/bracket       bracket_order_update
         │                      │                      │
         └──────────────────────┴──────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────┐
        │   Flask Application (app.py)       │
        │   - Routing                        │
        │   - Rate Limiting                  │
        │   - Request Validation             │
        └───────────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
    ┌─────────┐  ┌─────────────┐  ┌──────────┐
    │ REST API│  │ Webhook     │  │ Response │
    │ Endpoint│  │ Endpoint    │  │ Handler  │
    │(bracket_│  │(tv_json.py) │  │          │
    │order.py)│  │             │  │          │
    └────┬────┘  └──────┬──────┘  └──────────┘
         │               │
         └───────┬───────┘
                 │
                 ▼
    ┌─────────────────────────────────┐
    │  Bracket Order Service Layer     │
    │  (bracket_order_service.py)      │
    │                                  │
    │  • validate_bracket_order()      │
    │  • place_bracket_order()         │
    │  • place_bracket_order_with_auth│
    └──────────────┬────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
    ┌──────┐  ┌──────┐  ┌──────────┐
    │ Auth │  │Broker│  │ Database │
    │ DB   │  │ API  │  │ Logging  │
    └──────┘  └──────┘  └──────────┘
        │          │          │
        └──────────┼──────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
    Entry Order         GTT Orders
    (Immediate)         (Background)
        │                     │
        └──────────┬──────────┘
                   │
                   ▼
        ┌───────────────────────┐
        │  Broker Integrations  │
        │  (broker/*/api/)      │
        │                       │
        │  • place_order_api()  │
        │  • place_gtt_api()    │
        └───────────────────────┘
```

## Request Flow Diagram

```
User Request
    │
    ▼
API Endpoint
(bracket_order.py or tv_json.py)
    │
    ├─ Parse JSON
    ├─ Validate Schema (Marshmallow)
    └─ Rate Limit Check
    │
    ▼
Bracket Order Service
(bracket_order_service.py)
    │
    ├─ Extract API Key
    ├─ Get Auth Token
    └─ Validate Order Data
    │
    ▼
Place Entry Order
(broker_module.place_order_api)
    │
    ├─ Entry Order Success? ────NO──→ Error Response (400)
    │
    YES
    │
    ▼
Schedule GTT Orders (Background Thread)
    │
    ├─ Wait 2 seconds
    ├─ Place SL Order
    │  └─ Success? ─NO─→ Partial Failure
    │
    ├─ Place Target Order
    │  └─ Success? ─NO─→ Partial Failure
    │
    └─ All Success? ─YES─→ Emit Success Event
    │
    ▼
Return Response to Client
+ WebSocket Events
+ Telegram Notifications
+ Database Logging
```

## File Dependencies

```
bracket_order_service.py
├── Imports:
│   ├── database.auth_db (get_auth_token_broker)
│   ├── database.apilog_db (async_log_order)
│   ├── database.analyzer_db (async_log_analyzer)
│   ├── extensions (socketio)
│   ├── utils.constants (VALID_*)
│   ├── services.telegram_alert_service
│   └── broker.{broker_name}.api.order_api (place_order_api, place_gtt_order_api)
│
└── Used by:
    ├── restx_api.bracket_order (REST endpoint)
    └── blueprints.tv_json (Webhook endpoint)

bracket_order.py (REST API)
├── Imports:
│   ├── flask_restx (Namespace, Resource)
│   ├── marshmallow (ValidationError, Schema, fields)
│   ├── services.bracket_order_service
│   ├── database.apilog_db (async_log_order)
│   └── limiter
│
└── Registered in:
    └── restx_api/__init__.py (api.add_namespace)

tv_json.py (Webhook)
├── Imports:
│   ├── flask (Blueprint, request, jsonify)
│   ├── services.bracket_order_service
│   ├── database.symbol (enhanced_search_symbols)
│   └── database.auth_db (get_api_key_for_tradingview)
│
└── New route:
    └── /tradingview/webhook/bracket (POST)

__init__.py (API Registration)
├── Imports:
│   └── .bracket_order (api as bracket_order_ns)
│
└── Registers:
    └── api.add_namespace(bracket_order_ns, '/placebracketorder')
```

## Data Flow

### Request Payload
```
{
    "apikey": "string"              ─→ Authentication
    "symbol": "string"              ─→ Symbol validation
    "exchange": "string"            ─→ Exchange validation
    "product": "string"             ─→ Product validation
    "action": "string"              ─→ BUY/SELL validation
    "quantity": "integer"           ─→ Quantity validation
    "entry_price": "float"          ─┐
    "sl_price": "float"             ├─→ Price relationship validation
    "target_price": "float"         ─┘
    "optional fields"               ─→ Order type details
}
```

### Processing Steps

1. **Request Validation**
   - Schema validation (Marshmallow)
   - Field presence check
   - Data type validation
   - Rate limit check

2. **Authentication**
   - API key lookup
   - Token retrieval
   - Broker identification

3. **Business Logic Validation**
   - Price relationship check
   - Quantity validation
   - Exchange validation
   - Action validation

4. **Order Placement**
   - Create entry order data
   - Call broker API
   - Get order ID
   - Store order ID

5. **Background Processing**
   - Schedule GTT order thread
   - Wait for confirmation
   - Place SL order
   - Place Target order
   - Handle success/failure

6. **Response & Notification**
   - Return success/error response
   - Emit WebSocket event
   - Send Telegram alert (if configured)
   - Log to database

## Integration with Existing Systems

### Authentication Integration
```
bracket_order_service.py
    └─ get_auth_token_broker(api_key)
        └─ database/auth_db.py
            └─ Looks up user by API key
            └─ Returns (auth_token, broker)
```

### Broker Integration
```
bracket_order_service.py
    └─ import_broker_module(broker)
        └─ Dynamically imports broker.{broker}.api.order_api
            └─ place_order_api(order_data, auth_token)
            └─ place_gtt_order_api(gtt_data, auth_token) [Optional]
```

### Database Integration
```
bracket_order_service.py
    └─ async_log_order(api_type, request, response)
        └─ database/apilog_db.py
            └─ Logs to order_logs table asynchronously
```

### Notification Integration
```
bracket_order_service.py
    ├─ socketio.emit('bracket_order_update', data)
    │   └─ extensions.py (WebSocket)
    │       └─ Real-time client updates
    │
    └─ telegram_alert_service.send_order_alert(...)
        └─ services/telegram_alert_service.py
            └─ Telegram notifications
```

### Rate Limiting Integration
```
restx_api/bracket_order.py
    └─ @limiter.limit(BRACKET_ORDER_RATE_LIMIT)
        └─ limiter.py
            └─ Flask-Limiter instance
```

## Environment Variable Integration

```python
# .env Configuration
BRACKET_ORDER_RATE_LIMIT = os.getenv("BRACKET_ORDER_RATE_LIMIT", "2 per second")
BRACKET_ORDER_DELAY = os.getenv("BRACKET_ORDER_DELAY", "0.5")

# Database URL (for logging)
DATABASE_URL = os.getenv('DATABASE_URL')

# Broker API credentials (per user/session)
# Retrieved from auth_db.get_auth_token_broker(api_key)
```

## API Registration Flow

```
app.py
├─ from restx_api import api_v1_bp
├─ app.register_blueprint(api_v1_bp)
│
└─ restx_api/__init__.py
   ├─ from .bracket_order import api as bracket_order_ns
   ├─ api.add_namespace(bracket_order_ns, path='/placebracketorder')
   │
   └─ Results in:
      POST /api/v1/placebracketorder/
```

## Event Emission Points

```
bracket_order_service.py
├─ Emit "bracket_order_update" with status:
│  ├─ "entry_order_placed"
│  ├─ "completed"
│  ├─ "partial_failure"
│  └─ "error"
│
└─ Connected to:
   └─ extensions.py → socketio instance
      └─ Client-side listeners
```

## Database Schema Integration

```
order_logs table (apilog_db.py)
├─ id (Primary Key)
├─ api_type = 'placebracketorder'
├─ request_data (JSON)
│  └─ Contains: symbol, exchange, action, quantity, prices
├─ response_data (JSON)
│  └─ Contains: status, order_ids, error messages
└─ created_at (Timestamp)
```

## Configuration Parameters

```yaml
Bracket Order Configuration:
  - BRACKET_ORDER_RATE_LIMIT: "2 per second"
  - BRACKET_ORDER_DELAY: "0.5" seconds
  
Entry Order Parameters:
  - pricetype: "LIMIT"
  - ordertype: "REGULAR"
  - validity: "DAY" (configurable)
  
GTT Order Parameters:
  - order_type: "GTT"
  - Depends on broker support
  
Validation Parameters:
  - VALID_EXCHANGES: [NSE, BSE, MCX, NCDEX, FOREX]
  - VALID_ACTIONS: [BUY, SELL]
  - VALID_PRODUCT_TYPES: [MIS, CNC, NRML]
  - VALID_PRICE_TYPES: [LIMIT, MARKET, SL, SL-M]
```

## Error Handling Flow

```
Error Occurs
    │
    ├─ Validation Error (400)
    │  └─ Return: {"status": "error", "message": "..."}
    │
    ├─ Authentication Error (401)
    │  └─ Return: {"status": "error", "message": "Invalid API key"}
    │
    ├─ Broker Error (500)
    │  └─ Return: {"status": "error", "message": "Broker API error"}
    │
    └─ Partial Success
       └─ Return: {"status": "success", "message": "Entry order placed..."}
          └─ Background thread fails silently (logs to DB, emits event)
```

## Deployment Considerations

### Required Services
- Flask application running
- Database (SQLite/PostgreSQL) for logging
- Broker API endpoints accessible
- Redis (if using session management)
- Telegram bot (if notifications enabled)

### Optional Services
- WebSocket proxy (for real-time updates)
- Message queue (for async order processing)
- Cache layer (Redis for performance)

### System Requirements
- Python 3.7+
- Flask-RESTX
- Marshmallow
- Threading support (for background GTT placement)
- Database driver (sqlite3 or psycopg2)

---

**Architecture Design**: Multi-layered with service separation  
**Integration Pattern**: Modular with dependency injection  
**Data Flow**: Request → Service → Broker → Response  
**Error Handling**: Comprehensive with partial failure support  
**Notifications**: Multi-channel (WebSocket, Telegram, Database)

