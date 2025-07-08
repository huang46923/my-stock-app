import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.title("📈 Goodinfo 股利與財報爬蟲 (超詳細 debug 版)")

# 🟠 這裡是你要填的 Goodinfo Cookie
headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": "__qca=I0-1495454544-1751959713398; CLIENT%5FID=20250424103910203%5F36%2E236%2E226%2E252; _ga=GA1.1.456343899.1745462354; _cc_id=45f72cd985475675e8078c8715a36c3a; jiyakeji_uuid=72485dc0-20b5-11f0-aee0-4fdc55ea143b; IS_TOUCH_DEVICE=F; SCREEN_SIZE=WIDTH=1536&HEIGHT=864; TW_STOCK_BROWSE_LIST=2330%7C6605%7C2379; panoramaId_expiry=1752564414281; panoramaId=67c443d7a4a7f7e8713f599af84216d539389231111e439effbe89ef4a99d0e7; panoramaIdType=panoIndiv; LOGIN=EMAIL=jenda88%40gmail%2Ecom&USER%5FNM=%E9%BB%83%E5%A4%A7&ACCOUNT%5FID=115588689002630822587&ACCOUNT%5FVENDOR=Google&NO%5FEXPIRE=T; cto_bidid=9NDXO19Ya042U1FEb2t6VDNRMGI1SEVKc08zWVZFRGUzQVglMkJCZ1VFM2RJcVJwdTMxWEd2UlZLaFc4SUcwTmJjcnVZMlZNSm9ObVpqZlBmQTlHbW9TOUZya0ozbzRjTmxNdHFvUW5WcDk0JTJCUENkYVElM0Q; __gads=ID=7b2c5d9d0eba7f53:T=1745462357:RT=1751969619:S=ALNI_Ma8Bu60JC-JhjO0L5bhCeOvMdezZA; __gpi=UID=00001011c76ffed1:T=1745462357:RT=1751969619:S=ALNI_MYOaMOP2BWWyg7PQWSOS-wZts3DUg; __eoi=ID=56fde6102b8db0bc:T=1745462357:RT=1751969619:S=AA-AfjYcKcwZN3Ng6W61dvg7-kdx; _ga_0LP5MLQS7E=GS2.1.s1751969313$o5$g1$t1751969622$j54$l0$h0; FCNEC=%5B%5B%22AKsRol-BORhhrk3oByhr0R17uB6x1WdUIAlamWPW3AjL-4Bag30n2ix1OTpno6DXYzXNfpOFcIZwXD4A3vrarfs4ri80bHHxAjZ3b54LUG6rEXEOG2V5EpY4d_qeBpdgSxEmNVuc1M-qhwV3CPyrscPh70u_zz8m6Q%3D%3D%22%5D%5D; cto_bundle=cHggRV9Rd3dHTlJqMld3TkZMaSUyRnd6YlRaRyUyRktqN1RUNkNPVGVRayUyRkVEVkJ3OW1RTll2cVJDU2IwOSUyRnprVXpMQTNwODR5WDZva2h3eTRxN3NqMnRUU1ElMkZkbmZEVEYlMkJtOUhkN2xYZHNsNkxVRmk5Sk9HYiUyQllmbDZTZ2xVRDVZRnlGeW1wcko5cCUyQllocHRiUWdrVXVJeFVpekdnJTNEJTNE"
}

def fetch_table(url):
    """
    用 requests + BeautifulSoup 下載並解析表格
    """
    print(f"🌐 嘗試請求 URL: {url}")
    try:
        response = requests.get(url, headers=headers)
        print(f"✅ HTTP 狀態碼: {response.status_code}")
    except Exception as e:
        print(f"❗ 請求錯誤: {e}")
        return pd.DataFrame()

    if response.status_code != 200:
        print(f"❗️ 無法連線，HTTP 狀態碼: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")

    # 偵錯用: 輸出部分 HTML
    print("✅ [DEBUG] 取得的部分 HTML:")
    print(response.text[:1000])  # 避免太長

    tables = soup.find_all("table")
    print(f"✅ 找到 {len(tables)} 張表")

    if not tables:
        print("❗️ 沒有表格可供解析")
        return pd.DataFrame()

    try:
        df = pd.read_html(str(tables[0]))[0]
        print("✅ 解析成功")
        return df
    except Exception as e:
        print(f"❗️ 解析錯誤: {e}")
        return pd.DataFrame()

def fetch_data(stock_id):
    """
    抓 Goodinfo 三種表格
    """
    urls = {
        "財務比率": f"https://goodinfo.tw/tw/StockFinRatio.asp?STOCK_ID={stock_id}",
        "股利政策": f"https://goodinfo.tw/tw/StockDividendPolicy.asp?STOCK_ID={stock_id}",
        "現金流量": f"https://goodinfo.tw/tw/StockCashFlow.asp?STOCK_ID={stock_id}"
    }

    all_dfs = []
    for name, url in urls.items():
        st.write(f"🔗 正在抓取: {name}")
        df = fetch_table(url)
        if not df.empty:
            df["來源"] = name
            all_dfs.append(df)
        else:
            st.warning(f"⚠️ 無法取得 {name} 資料")

    if all_dfs:
        result = pd.concat(all_dfs, ignore_index=True)
        print(f"✅ 最終合併結果筆數: {len(result)}")
        return result
    else:
        print("❗️ 所有表格都抓不到")
        return pd.DataFrame()

# -----------------------------
# Streamlit UI
# -----------------------------
stock_id = st.text_input("請輸入股票代碼", "2330")

if st.button("🚀 抓取資料"):
    st.info(f"開始抓取股票代碼：{stock_id}")
    data = fetch_data(stock_id)
    if not data.empty:
        st.success("✅ 抓取成功！以下是結果：")
        st.dataframe(data)
    else:
        st.error("❗ 無法取得任何資料，請檢查 Cookie 或稍後再試")
