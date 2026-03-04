COINBASE REAL-TIME QUANTITATIVE RISK ENGINE

Crypto apps only show whether prices are going up or down. This terminal acts like a “Risk GPS,” using math to measure whether the market is behaving normally or showing unusual and potentially dangerous movement. Cnnects directly to Coinbase to analyze live price data for assets like Bitcoin, Ethereum, and Solana.

Key Features:

1) Volatility Alert (Z-Score): Shows whether current market activity is more chaotic than usual.
2) Efficiency Score (Sharpe Ratio): Measures how much return you are getting relative to the risk you are taking.
3) Multi-Asset View: Monitor several cryptocurrencies on one screen and see how they move together.

How It Works:

The project has two main parts:

1) tracker_engine.py: Connects to Coinbase market data, downloads and processes live price information, performs risk and statistical calculations.

2) app.py: Converts engine outputs into interactive charts and displays data.
