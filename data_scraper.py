import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_data(stock_id):
    """
    從 Goodinfo 爬取台股近五年的 ROE、股息發放率、自由現金流
    回傳 pandas DataFrame
    """

    # 這裡示範用「假資料」格式
    # 你可以改成真正的爬蟲解析程式碼

    years = [2020, 2021, 2022, 2023, 2024]
    roe = [15.2, 17.1, 19.8, 18.3, 16.5]
    payout_ratio = [0.35, 0.4, 0.38, 0.36, 0.34]
    fcf = [500, 520, 480, 510, 495]

    df = pd.DataFrame({
        'Year': years,
        'ROE': roe,
        'DividendPayoutRatio': payout_ratio,
        'FCF': fcf
    })

    return df
