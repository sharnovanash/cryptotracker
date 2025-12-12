import ccxt
import pandas as pd
import numpy as np
from datetime import datetime

class CryptoVolatilityTracker:
    def __init__(self, symbol='BTC/USD', window=20):
        #coinbase pro
        self.exchange = ccxt.coinbaseexchange({'enableRateLimit': True})
        self.symbol = symbol
        self.window = window
        self.ann_factor = np.sqrt(525600) 

    def fetch_data(self):
        try:
            bars = self.exchange.fetch_ohlcv(self.symbol, timeframe='1m', limit=300)
            df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'volume'])
            df['ts'] = pd.to_datetime(df['ts'], unit='ms')
            return df
        except Exception as e:
            print(f"Connection Error: {e}")
            return None

    def calculate_metrics(self, df):
        if df is None or len(df) < self.window:
            return df

        #lof returns
        df['returns'] = np.log(df['close'] / df['close'].shift(1))
        
        #volatility
        df['vol'] = df['returns'].rolling(window=self.window).std()
        
        #annualized
        df['ann_vol'] = df['vol'] * self.ann_factor * 100

        v_mean = df['vol'].rolling(window=self.window).mean()
        v_std = df['vol'].rolling(window=self.window).std()
        df['vol_z'] = (df['vol'] - v_mean) / v_std
        
        #sharpe ratio
        rf_min = 0.02 / 525600 
        rolling_ret = df['returns'].rolling(window=self.window).mean()
        # Sharpe = (Return - RF) / Standard Deviation
        df['sharpe'] = (rolling_ret - rf_min) / (df['vol'] + 1e-9) # Added epsilon to avoid div by zero
        
        #MDD
        roll_max = df['close'].rolling(window=self.window, min_periods=1).max()
        df['drawdown'] = (df['close'] / roll_max) - 1.0
    
        return df.dropna().reset_index(drop=True)