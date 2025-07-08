import streamlit as st
import pandas as pd
from data_scraper import fetch_data
from compute import compute_g
from plotter import plot_chart

# Streamlit App 主程式
st.set_page_config(page_title="Taiwan Stock ROE / g / FCF Analyzer", layout="centered")

st.title("Taiwan Stock ROE / g / FCF Analyzer 📈")

st.write("Enter a Taiwan stock ID to see 5-year ROE, Dividend Payout Ratio, g, and Free Cash Flow trends.")

# 使用者輸入
stock_id = st.text_input("Enter Stock ID", value="2330")

if st.button("Search"):
    with st.spinner('Fetching data...'):
        # 取得資料
        df = fetch_data(stock_id)
        df = compute_g(df)

        # 顯示表格
        st.subheader(f"{stock_id} - Financial Data")
        st.dataframe(df)

        # 畫圖
        st.subheader("Trend Chart")
        fig = plot_chart(df, stock_id)
        st.pyplot(fig)
