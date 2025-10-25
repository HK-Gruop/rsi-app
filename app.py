import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator  # pip install ta
import streamlit as st

st.set_page_config(page_title="RSI > 60 Stock Scanner", layout="wide")
st.title("📈 RSI > 60 Stock Scanner (Monthly Data)")
st.write("This app fetches monthly RSI values for selected NSE stocks using Yahoo Finance.")

tickers = {
    "SONACOMS.NS": "SONACOMS",
    "GODREJCP.NS": "GODREJCP",
    "NBCC.NS": "NBCC",
    "MFSL.NS": "MFSL",
    "TATACHEM.NS": "TATACHEM",
    "UNITDSPR.NS": "UNITDSPR",
    "BPCL.NS": "BPCL",
    "KALYANKJIL.NS": "KALYANKJIL",
    "JINDALSTEL.NS": "JINDALSTEL",
    "RECLTD.NS": "RECLTD",
    "NESTLEIND.NS": "NESTLEIND",
    "CROMPTON.NS": "CROMPTON",
    "TATACONSUM.NS": "TATACONSUM",
    "OBEROIRLTY.NS": "OBEROIRLTY",
    "UNOMINDA.NS": "UNOMINDA",
    "HCLTECH.NS": "HCLTECH",
    "PGEL.NS": "PGEL",
    "CONCOR.NS": "CONCOR",
    "LAURUSLABS.NS": "LAURUSLABS",
    "NTPC.NS": "NTPC",
    "TATASTEEL.NS": "TATASTEEL",
    "HINDPETRO.NS": "HINDPETRO",
    "PPLPHARMA.NS": "PPLPHARMA",
    "TECHM.NS": "TECHM",
    "GODREJPROP.NS": "GODREJPROP",
    "ICICIPRULI.NS": "ICICIPRULI",
    "FORTIS.NS": "FORTIS",
    "MAXHEALTH.NS": "MAXHEALTH",
    "PHOENIXLTD.NS": "PHOENIXLTD",
    "VOLTAS.NS": "VOLTAS",
    "HDFCLIFE.NS": "HDFCLIFE",
    "NMDC.NS": "NMDC",
    "CIPLA.NS": "CIPLA",
    "SBILIFE.NS": "SBILIFE",
    "BHARATFORG.NS": "BHARATFORG",
    "RBLBANK.NS": "RBLBANK",
    "OIL.NS": "OIL",
    "INFY.NS": "INFY",
    "ICICIBANK.NS": "ICICIBANK",
    "ASTRAL.NS": "ASTRAL",
    "NATIONALUM.NS": "NATIONALUM",
    "ADANIENSOL.NS": "ADANIENSOL",
    "SHRIRAMFIN.NS": "SHRIRAMFIN",
    "BAJAJFINSV.NS": "BAJAJFINSV",
    "INDUSTOWER.NS": "INDUSTOWER",
    "LUPIN.NS": "LUPIN",
    "VEDL.NS": "VEDL",
    "BEL.NS": "BEL",
    "HINDZINC.NS": "HINDZINC",
    "MOTHERSON.NS": "MOTHERSON",
    "SUNPHARMA.NS": "SUNPHARMA",
    "AUROPHARMA.NS": "AUROPHARMA",
    "MARICO.NS": "MARICO",
    "LICI.NS": "LICI",
    "IGL.NS": "IGL",
    "CYIENT.NS": "CYIENT",
    "AUBANK.NS": "AUBANK",
    "HDFCBANK.NS": "HDFCBANK",
    "HINDALCO.NS": "HINDALCO",
    "PAYTM.NS": "PAYTM",
    "PFC.NS": "PFC",
    "POWERGRID.NS": "POWERGRID",
    "BIOCON.NS": "BIOCON",
    "EXIDEIND.NS": "EXIDEIND",
    "ASHOKLEY.NS": "ASHOKLEY",
    "KFINTECH.NS": "KFINTECH",
    "PNB.NS": "PNB",
    "IOC.NS": "IOC",
    "CDSL.NS": "CDSL",
    "ADANIPORTS.NS": "ADANIPORTS",
    "UPL.NS": "UPL",
    "JSWSTEEL.NS": "JSWSTEEL",
    "SAMMAANCAP.NS": "SAMMAANCAP",
    "LODHA.NS": "LODHA",
    "INOXWIND.NS": "INOXWIND",
    "INDHOTEL.NS": "INDHOTEL",
    "ETERNAL.NS": "ETERNAL",
    "PATANJALI.NS": "PATANJALI",
    "CANBK.NS": "CANBK",
    "AMBUJACEM.NS": "AMBUJACEM",
    "IEX.NS": "IEX",
    "WIPRO.NS": "WIPRO",
    "TATATECH.NS": "TATATECH",
    "NYKAA.NS": "NYKAA",
    "LTF.NS": "LTF",
    "ONGC.NS": "ONGC",
    "AXISBANK.NS": "AXISBANK",
    "ICICIGI.NS": "ICICIGI",
}

# Convert dict to lists
stock_names = list(tickers.values())
symbols = list(tickers.keys())

rsi_stocks = []
progress_bar = st.progress(0)
status_text = st.empty()

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

if rsi_stocks:
    result_df = pd.DataFrame(rsi_stocks, columns=["Stock Name", "Symbol", "RSI"])
    result_df = result_df.sort_values(by="RSI", ascending=False)

    st.success("✅ Stocks with RSI > 60 (Monthly Data)")
    st.dataframe(result_df, use_container_width=True)

    # Option to download
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "RSI_above_60.csv", "text/csv")

else:
    st.error("⚠️ No stocks found with RSI > 60")
