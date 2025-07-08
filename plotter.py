import matplotlib.pyplot as plt

def plot_chart(df, stock_id):
    """
    繪製雙軸折線圖
    - 左Y軸：ROE、g
    - 右Y軸：自由現金流(FCF)
    - 所有標題、座標軸文字以英文顯示
    - 轉折點上顯示數值
    """

    # 建立圖表和主軸
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 設定主軸
    ax1.set_xlabel('Year')
    ax1.set_ylabel('ROE / g (%)', color='black')
    ax1.plot(df['Year'], df['ROE'], color='blue', marker='o', label='ROE')
    ax1.plot(df['Year'], df['g'], color='green', marker='o', label='g')
    ax1.tick_params(axis='y', labelcolor='black')

    # 在ROE和g的轉折點顯示數值
    for x, y in zip(df['Year'], df['ROE']):
        ax1.text(x, y, f'{y:.1f}', color='blue', fontsize=8, ha='center', va='bottom')
    for x, y in zip(df['Year'], df['g']):
        ax1.text(x, y, f'{y:.1f}', color='green', fontsize=8, ha='center', va='bottom')

    ax1.legend(loc='upper left')

    # 建立右側次軸
    ax2 = ax1.twinx()
    ax2.set_ylabel('Free Cash Flow', color='black')
    ax2.plot(df['Year'], df['FCF'], color='red', marker='o', label='FCF')
    ax2.tick_params(axis='y', labelcolor='black')

    # 在FCF的轉折點顯示數值
    for x, y in zip(df['Year'], df['FCF']):
        ax2.text(x, y, f'{y:.0f}', color='red', fontsize=8, ha='center', va='bottom')

    ax2.legend(loc='upper right')

    # 圖表標題
    plt.title(f'{stock_id} - ROE, g, and Free Cash Flow (5-year Trend)', fontsize=14)
    plt.tight_layout()

    return fig
