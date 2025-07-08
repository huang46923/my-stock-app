import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# ✅ 這裡貼上你的 Cookie
MY_COOKIE = "LUQJO0EJ-2-DXK; khaos_p=LUQJO0EJ-2-DXK; receive-cookie-deprecation=1; audit_p=1|WD0cx+9RTMJJoGjx1GgwIgTRTvNIFW7pouUc6SIN08/PgfFSMcnIh25M6x5w/b6Vcpj76PKZXj8ZA/WIsjdMLUKR6H9/9G798V0kxMR6Y5FfW8pPU411Fg==; audit=1|WD0cx+9RTMJJoGjx1GgwIgTRTvNIFW7pouUc6SIN08/PgfFSMcnIh25M6x5w/b6Vcpj76PKZXj8ZA/WIsjdMLUKR6H9/9G798V0kxMR6Y5FfW8pPU411Fg=="

headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": MY_COOKIE
}

@st.cache_data
def fetch_data(stock_id):
    url = f"https://goodinfo.tw/tw/StockFinRatio.asp?STOCK_ID={stock_id}"
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'

    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.find('table')
    if table is None:
        st.error("⚠️ 找不到財務表。請確認 Cookie 是否有效。")
        return pd.DataFrame()

    df = pd.read_html(str(table))[0]
    return df

st.title("📈 Goodinfo 財報擷取")

stock_id = st.text_input("輸入股票代碼", "2330")

if st.button("抓取資料"):
    with st.spinner("抓取中..."):
        df = fetch_data(stock_id)
        if not df.empty:
            st.dataframe(df)
