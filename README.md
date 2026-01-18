# AlgoSattva - Algorithmic Trading Platform

<div align="center">

**Powered by [OpenAlgo](https://github.com/marketcalls/openalgo)**

</div>

![AlgoSattva - Your Personal Algo Trading Platform](static/images/image.png)

**AlgoSattva** is a production-ready algorithmic trading platform built with Flask and Python. It provides a unified API layer across 24+ Indian brokers, enabling seamless integration with popular platforms like TradingView, Amibroker, Excel, Python, and AI agents. Designed for traders and developers, AlgoSattva makes algo trading accessible, secure, and powerful.

## About

AlgoSattva is a rebranded version of [OpenAlgo](https://github.com/marketcalls/openalgo), an open-source algorithmic trading platform. This project maintains full compliance with the AGPL-3.0 license.

## Quick Links

- **Original Project**: [OpenAlgo on GitHub](https://github.com/marketcalls/openalgo)
- **OpenAlgo Documentation**: [docs.openalgo.in](https://docs.openalgo.in)
- **Installation Guide**: [Getting Started](https://docs.openalgo.in/installation-guidelines/getting-started)

## Python Compatibility

**Supports Python 3.11, 3.12, 3.13, and 3.14**

## Supported Brokers (24+)

<details>
<summary>View All Supported Brokers</summary>

- 5paisa (Standard + XTS)
- AliceBlue
- AngelOne
- Compositedge
- Definedge
- Dhan (Live + Sandbox)
- Firstock
- Flattrade
- Fyers
- Groww
- IBulls
- IIFL
- Indmoney
- JainamXTS
- Kotak Neo
- Motilal Oswal
- Mstock
- Paytm Money
- Pocketful
- Samco
- Shoonya (Finvasia)
- Tradejini
- Upstox
- Wisdom Capital
- Zebu
- Zerodha

</details>

All brokers share a unified API interface, making it easy to switch between brokers without changing your code.

## Core Features

### Unified REST API Layer (`/api/v1/`)
A single, standardized API across all brokers with 30+ endpoints:
- **Order Management**: Place, modify, cancel orders, basket orders, smart orders with position sizing
- **Portfolio**: Get positions, holdings, order book, trade book, funds
- **Market Data**: Real-time quotes, historical data, market depth (Level 5), symbol search
- **Advanced**: Option Greeks calculator, margin calculator, synthetic futures, auto-split orders

### Real-Time WebSocket Streaming
- Unified WebSocket proxy server for all brokers (port 8765)
- Common WebSocket implementation using ZMQ for normalized data across brokers
- Subscribe to LTP, Quote, or Market Depth for any symbol
- ZeroMQ-based message bus for high-performance data distribution
- Automatic reconnection and failover handling

### API Analyzer Mode
Complete testing environment with ₹1 Crore virtual capital:
- Test strategies with real market data without risking money
- Pre-deployment testing for strategy validation
- Supports all order types (Market, Limit, SL, SL-M)
- Realistic margin system with leverage
- Auto square-off at exchange timings
- Separate database for complete isolation

### Action Center
Order approval workflow for manual control:
- **Auto Mode**: Immediate order execution (for personal trading)
- **Semi-Auto Mode**: Manual approval required before broker execution
- Complete audit trail with IST timestamps
- Approve individual orders or bulk approve all

## Installation

Please refer to the [OpenAlgo Documentation](https://docs.openalgo.in/installation-guidelines/getting-started) for detailed installation instructions.

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

### Attribution

This software is based on [OpenAlgo](https://github.com/marketcalls/openalgo), an open-source algorithmic trading platform created by [marketcalls](https://github.com/marketcalls).

- Original Project: https://github.com/marketcalls/openalgo
- Original License: AGPL-3.0

As required by the AGPL-3.0 license:
- The original copyright and license notices are preserved
- This modified version is also licensed under AGPL-3.0
- The source code is available at: https://github.com/code-python-in/algosattva

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This software is for educational and informational purposes only. Trading in financial markets involves substantial risk of loss. Past performance is not indicative of future results. Always do your own research and consult with a qualified financial advisor before making any investment decisions.
