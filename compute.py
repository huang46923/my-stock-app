def compute_g(df):
    """
    根據公式計算 g = ROE * (1 - 股息發放率)
    """
    df['g'] = df['ROE'] * (1 - df['DividendPayoutRatio'])
    return df
