import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_data(stock_id):
    """
    從 Goodinfo.tw 抓取台股近5年
    - 股東權益報酬率
    - 盈餘分配率(%)（從盈餘分配率統計「合計」欄抓）
    - 自由現金流
    回傳 pandas DataFrame
    """

    url = f"https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=XX&STOCK_ID={stock_id}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"❗️ 網頁請求失敗: {e}")
        return pd.DataFrame()

    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all('table')

    # 找到含股東權益報酬率和盈餘分配率統計關鍵字的表
    target_table = None
    for table in tables:
        table_text = table.text.replace(' ', '')
        if '股東權益報酬率' in table_text and '盈餘分配率統計' in table_text:
            target_table = table
            break

    if target_table is None:
        print("❗️ 找不到含 股東權益報酬率 / 盈餘分配率統計 的表格")
        return pd.DataFrame()

    rows = target_table.find_all('tr')

    years = []
    roe_values = []
    payout_values = []
    fcf_values = []

    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all(['th', 'td'])]
        if len(cols) < 8:
            continue

        # 年度
        try:
            year = int(cols[0])
        except ValueError:
            continue

        if len(years) >= 5:
            break

        # 股東權益報酬率
        try:
            roe = float(cols[1].replace('%','').replace(',',''))
        except:
            roe = None

        # 盈餘分配率 ➜ 右側的「盈餘分配率統計 ➜ 合計(%)」欄
        try:
            payout = float(cols[-1].replace('%','').replace(',',''))
            payout = payout / 100
        except:
            payout = None

        # 自由現金流
        try:
            fcf = float(cols[3].replace(',',''))
        except:
            fcf = None

        years.append(year)
        roe_values.append(roe)
        payout_values.append(payout)
        fcf_values.append(fcf)

    if not years:
        print("❗️ 解析到的資料是空的")
        return pd.DataFrame()

    df = pd.DataFrame({
        'Year': years,
        'ROE': roe_values,
        'DividendPayoutRatio': payout_values,
        'FCF': fcf_values
    })

    return df
