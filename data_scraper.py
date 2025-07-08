import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def parse_policy_text(policy_text):
    """
    從「股利政策」欄位裡解析「盈餘分配率」數值
    例如「盈餘分配率60%」 ➜ 0.6
    """
    if not policy_text:
        return None
    policy_text = policy_text.replace('％', '%').replace(' ', '').strip()
    match = re.search(r'盈餘分配率\s*([0-9]+(?:\.[0-9]+)?)%', policy_text)
    if match:
        return float(match.group(1)) / 100
    return None

def fetch_data(stock_id):
    """
    從 Goodinfo.tw 爬取台股近五年股東權益報酬率、股利政策（含盈餘分配率）、自由現金流
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

    # 找到含「股東權益」和「股利」關鍵字的表
    target_table = None
    for table in tables:
        table_text = table.text.replace('%','').replace(' ', '').lower()
        if '股東權益' in table_text and '股利' in table_text:
            target_table = table
            break

    if target_table is None:
        print("❗️ 找不到含股東權益/股利關鍵字的表格")
        return pd.DataFrame()

    # 解析表格
    rows = target_table.find_all('tr')
    years = []
    roe_values = []
    payout_values = []
    fcf_values = []

    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all(['th', 'td'])]
        if len(cols) < 4:
            continue

        try:
            year = int(cols[0])
        except ValueError:
            continue

        if len(years) >= 5:
            break

        # 解析 ROE
        try:
            roe = float(cols[1].replace('%','').replace(',',''))
        except:
            roe = None

        # 解析股利政策 ➜ 抓出「盈餘分配率」
        policy_text = cols[2]
        payout_ratio = parse_policy_text(policy_text)

        # 解析自由現金流
        try:
            fcf = float(cols[3].replace(',',''))
        except:
            fcf = None

        years.append(year)
        roe_values.append(roe)
        payout_values.append(payout_ratio)
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
