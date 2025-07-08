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

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"❗️ 網頁請求失敗: {e}")
        return pd.DataFrame()

    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all('table')

    # 尋找含有「ROE」或「股東權益報酬率」以及「股利發放率」的表格
    target_table = None
    for table in tables:
        table_text = table.text
        if (('ROE' in table_text or '股東權益報酬率' in table_text) and '股利發放率' in table_text):
            target_table = table
            break

    if target_table is None:
        print("❗️ 找不到含ROE/股東權益報酬率/股利發放率的表格")
        return pd.DataFrame()

    # 解析表格內容
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
