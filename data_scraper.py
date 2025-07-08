import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
}


def fetch_fin_ratio(stock_id):
    url = f"https://goodinfo.tw/tw/StockFinRatio.asp?STOCK_ID={stock_id}"
    print(f"✅ [DEBUG] Requesting 財務比率 URL: {url}")

    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    # 👉 不管有沒有找到表格都先印
    print("\n==== [FULL PAGE HTML - 財務比率表] ====")
    print(soup.prettify())

    # 找出財務比率表
    target_table = soup.find("table", class_="b1 p4_2 r10 box_shadow")
    if target_table is None:
        print("❗️ 找不到財務比率表")
        return pd.DataFrame()

    df = pd.read_html(str(target_table), flavor='bs4')[0]
    print("\n✅ [DEBUG] 財務比率表 DataFrame 取得成功：")
    print(df.head())

    # 只取最近5年
    df = df.iloc[:, :6]
    df = df.set_index(df.columns[0]).T
    df = df.rename_axis('Year').reset_index()

    df = df[['Year', '股東權益報酬率']]
    df = df.rename(columns={'股東權益報酬率': 'ROE'})

    print("\n✅ [DEBUG] 處理後 財務比率表 DataFrame：")
    print(df)

    return df


def fetch_dividend_policy(stock_id):
    url = f"https://goodinfo.tw/tw/StockDividendPolicy.asp?STOCK_ID={stock_id}"
    print(f"✅ [DEBUG] Requesting 股利政策 URL: {url}")

    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    # 👉 不管有沒有找到表格都先印
    print("\n==== [FULL PAGE HTML - 股利政策] ====")
    print(soup.prettify())

    # 找出「盈餘分配率統計」表
    target_table = soup.find("table", class_="b1 p4_2 r10 box_shadow")
    if target_table is None:
        print("❗️ 找不到 股利政策表")
        return pd.DataFrame()

    df = pd.read_html(str(target_table), flavor='bs4')[0]
    print("\n✅ [DEBUG] 股利政策表 DataFrame 取得成功：")
    print(df.head())

    # 只取最近5年
    df = df[df.columns[:6]]
    df.columns = df.columns.droplevel(0)
    df = df.rename(columns={'年度': 'Year', '盈餘配息率(%)': 'PayoutRatio'})
    df = df[['Year', 'PayoutRatio']].dropna()

    print("\n✅ [DEBUG] 處理後 股利政策表 DataFrame：")
    print(df)

    return df


def fetch_fcf(stock_id):
    url = f"https://goodinfo.tw/tw/StockCashFlow.asp?STOCK_ID={stock_id}"
    print(f"✅ [DEBUG] Requesting 現金流量 URL: {url}")

    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    # 👉 不管有沒有找到表格都先印
    print("\n==== [FULL PAGE HTML - 現金流量] ====")
    print(soup.prettify())

    # 找出自由現金流
    target_table = soup.find("table", class_="b1 p4_2 r10 box_shadow")
    if target_table is None:
        print("❗️ 找不到 現金流量表")
        return pd.DataFrame()

    df = pd.read_html(str(target_table), flavor='bs4')[0]
    print("\n✅ [DEBUG] 現金流量表 DataFrame 取得成功：")
    print(df.head())

    # 只取「每股自由現金流量」
    df = df[df.columns[:6]]
    df = df.set_index(df.columns[0]).T
    df = df.rename_axis('Year').reset_index()
    df = df[['Year', '每股自由現金流量(元)']]
    df = df.rename(columns={'每股自由現金流量(元)': 'FCF'})

    print("\n✅ [DEBUG] 處理後 現金流量表 DataFrame：")
    print(df)

    return df


def fetch_data(stock_id):
    print(f"\n🎯 [DEBUG] fetch_data 呼叫，Stock ID = {stock_id}")

    # 分別抓三段
    df_ratio = fetch_fin_ratio(stock_id)
    df_dividend = fetch_dividend_policy(stock_id)
    df_fcf = fetch_fcf(stock_id)

    if df_ratio.empty or df_dividend.empty or df_fcf.empty:
        print("❗️ [DEBUG] 有空表，無法合併")
        return pd.DataFrame()

    # 合併
    merged = pd.merge(df_ratio, df_dividend, on='Year', how='inner')
    merged = pd.merge(merged, df_fcf, on='Year', how='inner')

    # 計算 g
    merged['PayoutRatio'] = merged['PayoutRatio'] / 100
    merged['g'] = merged['ROE'] * (1 - merged['PayoutRatio'])

    print("\n✅ [DEBUG] 最後合併好的 DataFrame：")
    print(merged)

    return merged
