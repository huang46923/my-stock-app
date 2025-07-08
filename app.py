import streamlit as st
import pandas as pd
from data_scraper import fetch_data
from plotter import plot_chart

st.set_page_config(page_title="Taiwan Stock ROE / g / FCF Analyzer", layout="wide")

st.title("Taiwan Stock ROE / g / FCF Analyzer")
st.write("Enter a Taiwan stock ID to see 5-year ROE, Dividend Payout Ratio, g, and Free Cash Flow trends.")

stock_id = st.text_input("Enter Stock ID", value="")

if stock_id:
    st.write(f"✅ [DEBUG] User entered stock ID: {stock_id}")
    print(f"✅ [DEBUG] User entered stock ID: {stock_id}")

    if st.button("Search"):
        st.write(f"✅ [DEBUG] User clicked Search for stock_id: {stock_id}")
        print(f"✅ [DEBUG] User clicked Search for stock_id: {stock_id}")

        with st.spinner("Fetching data from Goodinfo..."):
            try:
                df = fetch_data(stock_id)
                print(f"✅ [DEBUG] fetch_data returned:\n{df}")

                if df.empty:
                    st.error("❗ 無法從 Goodinfo 抓到資料，請確認股票代碼或稍後再試")
                    print("❗ [DEBUG] Returned DataFrame is EMPTY")
                else:
                    st.success("✅ Data fetched successfully!")
                    st.write("### 📈 Data Table")
                    st.dataframe(df)

                    # Call plotting function
                    st.write("### 📊 Chart")
                    plot_chart(df)

            except Exception as e:
                st.error(f"❗ 發生錯誤：{e}")
                print(f"❗ [DEBUG] Exception in fetch_data: {e}")

else:
    st.info("請輸入股票代碼再按下 Search")
