import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Referer": "https://goodinfo.tw/tw/index.asp",
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8"
}


def fetch_url(url):
    print(f"\n🌐 [DEBUG] Fetching URL: {url}")
    time.sleep(2)  # ➜ 模擬人類點擊，不要被封
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    print(f"✅ [DEBUG] HTTP Status: {res.status_code}")
    return res.text


def parse_table(html, context):
    soup = BeautifulSoup(html, 'html.parser')
    print(f"\n==== [FULL PAGE HTML - {context}] ====")
    print(soup.prettify()[:2000])  # 避免太長

    table = soup.find("table", class_="b1 p4_2 r10 box_shadow")
    if table is None:
        print(f"❗️ [ERROR] 找不到表格 - {context}")
        return pd.DataFrame()

    df = pd.read_html(str(table), flavor='bs4')[0]
    print(f"✅ [DEBUG] 讀取 {context} 表成功")
    print(df.head())
    return df


def fetch_fin_ratio(stock_id):
    html = fetch_url(f"https://goodinfo.tw/tw/StockFinRatio.asp?STOCK_ID={stock_id}")
    df = parse_table(html, "財務比率表")
    if df.empty:
        return df

    df = df.iloc[:, :6]
    df = df.set_index(df.columns[0]).T
    df = df.rename_axis('Year').reset_index()
    df = df[['Year', '股東權益報酬率']]
    df = df.rename(columns={'股東權益報酬率': 'ROE'})
    return df


def fetch_dividend_policy(stock_id):
    html = fetch_url(f"https://goodinfo.tw/tw/StockDividendPolicy.asp?STOCK_ID={stock_id}")
    df = parse_table(html, "股利政策")
    if df.empty:
        return df

    df = df[df.columns[:6]]
    df.columns = df.columns.droplevel(0)
    df = df.rename(columns={'年度': 'Year', '盈餘配息率(%)': 'PayoutRatio'})
    df = df[['Year', 'PayoutRatio']].dropna()
    return df


def fetch_fcf(stock_id):
    html = fetch_url(f"https://goodinfo.tw/tw/StockCashFlow.asp?STOCK_ID={stock_id}")
    df = parse_table(html, "現金流量")
    if df.empty:
        return df

    df = df[df.columns[:6]]
    df = df.set_index(df.columns[0]).T
    df = df.rename_axis('Year').reset_index()
    df = df[['Year', '每股自由現金流量(元)']]
    df = df.rename(columns={'每股自由現金流量(元)': 'FCF'})
    return df


def fetch_data(stock_id):
    print(f"\n🎯 [DEBUG] fetch_data 呼叫，Stock ID = {stock_id}")

    df_ratio = fetch_fin_ratio(stock_id)
    df_dividend = fetch_dividend_policy(stock_id)
    df_fcf = fetch_fcf(stock_id)

    if df_ratio.empty or df_dividend.empty or df_fcf.empty:
        print("❗️ [DEBUG] 有空表，無法合併")
        return pd.DataFrame()

    merged = pd.merge(df_ratio, df_dividend, on='Year', how='inner')
    merged = pd.merge(merged, df_fcf, on='Year', how='inner')
    merged['PayoutRatio'] = merged['PayoutRatio'] / 100
    merged['g'] = merged['ROE'] * (1 - merged['PayoutRatio'])

    print("\n✅ [DEBUG] 最後合併好的 DataFrame：")
    print(merged)
    return merged
