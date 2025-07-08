import requests
from bs4 import BeautifulSoup
import pandas as pd

# 全域 debug 開關
DEBUG_MODE = False

def fetch_fin_ratio(stock_id):
    """
    從 財務比率表 抓 ROE 和 每股自由現金流量
    """
    url = f"https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=XX&STOCK_ID={stock_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"❗️ 財務比率表請求失敗: {e}")
        return pd.DataFrame()

    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    if DEBUG_MODE:
        print("\n==== 財務比率表 HTML ====")
        print(soup.prettify())

    tables = soup.find_all('table')

    target_table = None
    for table in tables:
        # 模糊匹配：避免官方微改版
        if '股東權益' in table.text and '自由現金流' in table.text:
            target_table = table
            break

    if target_table is None:
        print("❗️ 找不到 財務比率表")
        return pd.DataFrame()

    rows = target_table.find_all('tr')
    years, roe_values, fcf_values = [], [], []

    for row in rows:
        cols = [td.get_text(strip=True).replace(',', '').replace('%', '') for td in row.find_all(['th', 'td'])]
        if len(cols) < 6:
            continue
        if 'Q' in cols[0]:
            continue

        try:
            year = int(cols[0])
        except ValueError:
            continue

        try:
            roe = float(cols[1])
        except:
            roe = None

        try:
            fcf = float(cols[-1])
        except:
            fcf = None

        years.append(year)
        roe_values.append(roe)
        fcf_values.append(fcf)

    return pd.DataFrame({
        'Year': years,
        'ROE': roe_values,
        'FCF': fcf_values
    })


def fetch_dividend_policy(stock_id):
    """
    從 股利政策頁 抓 盈餘分配率(%) ➜ 只保留年度總合行
    固定指定 YEAR_MODE=發放年度
    """
    url = f"https://goodinfo.tw/tw/StockDividendPolicy.asp?STOCK_ID={stock_id}&YEAR_MODE=發放年度"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"❗️ 股利政策頁請求失敗: {e}")
        return pd.DataFrame()

    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    if DEBUG_MODE:
        print("\n==== 股利政策 HTML ====")
        print(soup.prettify())

    tables = soup.find_all('table')

    target_table = None
    for table in tables:
        # 模糊匹配關鍵字
        if '盈餘分配率' in table.text:
            target_table = table
            break

    if target_table is None:
        print("❗️ 找不到 股利政策表")
        return pd.DataFrame()

    rows = target_table.find_all('tr')
    years, payout_values = [], []

    for row in rows:
        cols = [td.get_text(strip=True).replace(',', '').replace('%', '') for td in row.find_all(['th', 'td'])]
        if len(cols) < 8:
            continue
        if 'Q' in cols[0]:
            continue

        try:
            year = int(cols[0])
        except ValueError:
            continue

        try:
            payout = float(cols[-1]) / 100
        except:
            payout = None

        years.append(year)
        payout_values.append(payout)

    return pd.DataFrame({
        'Year': years,
        'DividendPayoutRatio': payout_values
    })


def fetch_data(stock_id):
    """
    主函式：抓兩頁 ➜ 合併 ➜ 計算 g ➜ 顯示所有交集年份
    """
    print(f"\n🚀 正在抓取資料: {stock_id}")

    df_fin = fetch_fin_ratio(stock_id)
    if df_fin.empty:
        print("❗️ 財務比率表抓不到")
        return pd.DataFrame()

    df_div = fetch_dividend_policy(stock_id)
    if df_div.empty:
        print("❗️ 股利政策抓不到")
        return pd.DataFrame()

    if DEBUG_MODE:
        print("\n=== 抓到的 財務比率表 ===")
        print(df_fin)
        print("\n=== 抓到的 股利政策 ===")
        print(df_div)

    # 內聯結合併
    df = pd.merge(df_fin, df_div, on='Year', how='inner')
    if df.empty:
        print("❗️ 兩表合併後沒資料（年度交集為空）")
        return pd.DataFrame()

    # 計算 g
    df['g'] = df['ROE'] * (1 - df['DividendPayoutRatio'])

    # 顯示所有交集年份（不硬限制5筆）
    df = df.sort_values(by='Year', ascending=False).reset_index(drop=True)

    print("\n✅ 最終合併結果：")
    print(df)

    return df
