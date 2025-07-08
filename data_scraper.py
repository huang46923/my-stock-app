import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_data(stock_id):
    """
    從 Goodinfo.tw 爬取台股近五年ROE、股息發放率、自由現金流
    回傳 pandas DataFrame
    """

    url = f"https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=XX&STOCK_ID={stock_id}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # 發送GET請求
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'

    # 解析HTML
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all('table')

    # 找到含ROE資料的表格
    target_table = None
    for table in tables:
        if 'ROE' in table.text and '股利發放率' in table.text:
            target_table = table
            break

    if target_table is None:
        raise ValueError("❗️ 找不到含ROE/股利發放率的表格，請確認股票代碼正確")

    # 解析表格
    rows = target_table.find_all('tr')
    years = []
    roe_values = []
    payout_values = []
    fcf_values = []

    for row in rows:
        cols = [td.get_text(strip=True).replace(',', '').replace('%','') for td in row.find_all(['th', 'td'])]
        if len(cols) < 4:
            continue

        try:
            year = int(cols[0])
        except ValueError:
            continue

        # 只取近5年
        if len(years) >= 5:
            break

        try:
            roe = float(cols[1])
        except:
            roe = None

        try:
            payout = float(cols[2])
        except:
            payout = None

        try:
            fcf = float(cols[3])
        except:
            fcf = None

        years.append(year)
        roe_values.append(roe)
        payout_values.append(payout)
        fcf_values.append(fcf)

    # 建立DataFrame
    df = pd.DataFrame({
        'Year': years,
        'ROE': roe_values,
        'DividendPayoutRatio': payout_values,
        'FCF': fcf_values
    })

    return df
