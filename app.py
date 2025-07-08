import streamlit as st
import pandas as pd
from data_scraper import fetch_data
from compute import compute_g
from plotter import plot_chart

st.set_page_config(page_title="Taiwan Stock ROE / g / FCF Analyzer", layout="centered")

st.title("Taiwan Stock ROE / g / FCF Analyzer 📈")

st.write("Enter a Taiwan stock ID to see 5-year ROE, Dividend Payout Ratio, g, and Free Cash Flow trends.")

stock_id = st.text_input("Enter Stock ID", value="2330")

if st.button("Search"):
    with st.spinner('Fetching data...'):
        df = fetch_data(stock_id)

        if df.empty:
            st.error("❗️ 無法從 Goodinfo 抓到資料，請確認股票代碼或稍後再試")
        else:
            df = compute_g(df)
            st.subheader(f"{stock_id} - Financial Data")
            st.dataframe(df)

            st.subheader("Trend Chart")
            fig = plot_chart(df, stock_id)
            st.pyplot(fig)
