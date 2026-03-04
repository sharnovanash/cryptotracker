COINBASE REAL-TIME QUANTITATIVE RISK ENGINE

A a high-density analytical dashboard designed to bypass retail market sentiment. Utilizes statistical modeling to determine if current market behavior is within normal parameters or exhibiting high-risk anomalies. Connects directly to Coinbase to analyze live price data for assets like Bitcoin, Ethereum, and Solana.

Key Features:

1) Volatility Alert (Z-Score): Shows whether current market activity is more chaotic than usual.
2) Efficiency Score (Sharpe Ratio): Measures how much return you are getting relative to the risk you are taking.
3) Multi-Asset View: Monitor several cryptocurrencies on one screen and see how they move together.

How It Works:

1) tracker_engine.py: Connects to Coinbase market data, downloads and processes live price information, performs risk and statistical calculations
2) app.py: Converts engine outputs into interactive charts and displays data

Run:
1) Clone
2) Install Dependencies: pip install -r requirements.txt
3) Launch dashboard run the command streamlit run app.py
