import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tracker_engine import CryptoVolatilityTracker

import streamlit as st

st.set_page_config(page_title="CORE // TERMINAL", layout="wide")

st.markdown("""
    <style>
    /* Global Font & Background */
    * { font-family: 'Courier New', monospace !important; font-size: 0.82rem !important; }
    .stApp { background-color: #000000; }

    /* SIDEBAR AESTHETICS */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #333 !important;
        width: 250px !important;
    }
    
    /* Square every input/button in the sidebar */
    .stMultiSelect div, .stSlider div, .stSelectbox div, .stButton>button {
        border-radius: 0px !important;
        border-color: #444 !important;
        background-color: #0a0a0a !important;
    }

    /* Metric/Text color adjustments */
    [data-testid="stMetricValue"] { color: #00ff00 !important; font-size: 1.1rem !important; }
    [data-testid="stSidebarNav"] { display: none; } /* Hide default nav */
    
    /* Vertical Grid for Main Charts */
    .js-plotly-plot .gridlayer path {
        stroke: #222 !important; 
        stroke-width: 1px !important;
    }

    /* Adjusting the Sidebar Header */
    .sidebar-header {
        color: #00ff00;
        letter-spacing: 2px;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
        margin-bottom: 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

#sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-header">// CORE COMMAND</div>', unsafe_allow_html=True)
    
    #group inputs
    with st.container():
        st.caption("INSTRUMENT SELECT")
        selected_assets = st.multiselect(
            label="TICKERS",
            options=["BTC/USD", "ETH/USD", "SOL/USD", "AVAX/USD", "DOGE/USD"],
            default=["BTC/USD"],
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    
    with st.container():
        st.caption("CALIBRATION (N-PERIODS)")
        window = st.select_slider(
            "WINDOW", 
            options=[10, 20, 50, 100, 200], 
            value=20,
            label_visibility="collapsed"
        )

    st.markdown("---")
    
    st.caption("TELEMETRY")
    st.metric("LATENCY", "42ms", delta="-2ms")
    st.metric("FEED", "STABLE", delta_color="off")
    
    if st.button("RESET KERNEL", use_container_width=True):
        st.rerun()

#data processing
if selected_assets:
    master_data = {}
    for asset in selected_assets:
        tracker = CryptoVolatilityTracker(symbol=asset, window=window)
        data = tracker.fetch_data()
        if data is not None:
            master_data[asset] = tracker.calculate_metrics(data)

    if master_data:
        fig = make_subplots(
            rows=3, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.02,
            subplot_titles=("PRICE PERFORMANCE", "VOLATILITY Z-SCORE", "SHARPE (EFFICIENCY)"),
            row_heights=[0.5, 0.25, 0.25]
        )

        #iterate through assets
        for i, (asset, df) in enumerate(master_data.items()):
            color = "#00ff00" if i % 2 == 0 else "#ff0000"
            
            #subplot1:price
            fig.add_trace(go.Scatter(
                x=df['ts'], y=df['close'], 
                name=asset, line=dict(color=color, width=1.5)
            ), row=1, col=1)

            #subplot2:volatility z-score
            fig.add_trace(go.Scatter(
                x=df['ts'], y=df['vol_z'], 
                name=f"{asset} Vol", line=dict(color=color, width=1, dash='dot'),
                showlegend=False
            ), row=2, col=1)

            #subplot3:sharpe ratio
            fig.add_trace(go.Scatter(
                x=df['ts'], y=df['sharpe'], 
                name=f"{asset} Sharpe", line=dict(color=color, width=1.5),
                fill='tozeroy', showlegend=False
            ), row=3, col=1)

        #grid
        fig.update_layout(
            height=850,
            template="plotly_dark",
            paper_bgcolor='black',
            plot_bgcolor='black',
            margin=dict(l=10, r=10, t=40, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis3=dict(showgrid=True, gridcolor='#333', gridwidth=1), # Vertical Grid
            yaxis=dict(showgrid=True, gridcolor='#222'),
            yaxis2=dict(showgrid=True, gridcolor='#222'),
            yaxis3=dict(showgrid=True, gridcolor='#222')
        )
        
        #vertical grids
        fig.update_xaxes(showgrid=True, gridcolor='#333', gridwidth=1)
        
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("SYSTEM AUDIT // REAL-TIME")
        summary_rows = []
        for asset, df in master_data.items():
            latest = df.iloc[-1]
            summary_rows.append({
                "TICKER": asset,
                "LAST": f"${latest['close']:,.2f}",
                "ANN_VOL": f"{latest['ann_vol']:.2f}%",
                "Z_SCORE": round(latest['vol_z'], 2),
                "SHARPE": round(latest['sharpe'], 2)
            })
        st.dataframe(pd.DataFrame(summary_rows), hide_index=True, use_container_width=True)


        