import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
import streamlit as st

# Streamlit page setup
st.set_page_config(page_title="RSI > 60 Stock Scanner", page_icon="📈", layout="wide")

st.title("📈 RSI > 60 Stock Scanner (Monthly Data)")
st.write("This app fetches monthly RSI values for selected NSE stocks using Yahoo Finance.")

# Define stock dictionary
tickers = {
    "SONACOMS.NS": "SONACOMS",
    "BPCL.NS": "BPCL",
    "OBEROIRLTY.NS": "OBEROIRLTY",
    "CONCOR.NS": "CONCOR",
    "LAURUSLABS.NS": "LAURUSLABS",
    "NTPC.NS": "NTPC",
    "HINDPETRO.NS": "HINDPETRO",
    "TECHM.NS": "TECHM",
    "FORTIS.NS": "FORTIS",
    "INFY.NS": "INFY",
    "HDFCBANK.NS": "HDFCBANK",
    "PFC.NS": "PFC",
    "POWERGRID.NS": "POWERGRID",
    "ASHOKLEY.NS": "ASHOKLEY",
    "IOC.NS": "IOC",
    "JSWSTEEL.NS": "JSWSTEEL",
    "CANBK.NS": "CANBK",
    "TATATECH.NS": "TATATECH",
}

# Convert dict to lists
stock_names = list(tickers.values())
symbols = list(tickers.keys())

rsi_stocks = []
progress_bar = st.progress(0)
status_text = st.empty()

# Fetch RSI
for i, (symbol, stock_name) in enumerate(zip(symbols, stock_names)):
    try:
        status_text.text(f"Fetching data for {symbol} ({i+1}/{len(symbols)})...")
        df = yf.download(symbol, period="3y", interval="1mo", progress=False, auto_adjust=True)
        if df.empty or 'Close' not in df.columns:
            continue

        close_prices = df['Close'].squeeze()
        rsi_indicator = RSIIndicator(close=close_prices, window=14)
        df['RSI'] = rsi_indicator.rsi()

        last_rsi = df['RSI'].iloc[-1]
        if pd.notna(last_rsi) and last_rsi > 60:
            rsi_stocks.append((stock_name, symbol, round(last_rsi, 2)))
    except Exception as e:
        st.warning(f"⚠️ Error fetching {symbol}: {e}")

    progress_bar.progress((i + 1) / len(symbols))

progress_bar.empty()
status_text.empty()

# Display results
if rsi_stocks:
    result_df = pd.DataFrame(rsi_stocks, columns=["Stock Name", "Symbol", "RSI"])
    result_df = result_df.sort_values(by="RSI", ascending=False)

    st.success("✅ Stocks with RSI > 60 (Monthly Data)")
    st.dataframe(result_df, use_container_width=True)

    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "RSI_above_60.csv", "text/csv")
else:
    st.error("⚠️ No stocks found with RSI > 60")
