import matplotlib.pyplot as plt

def plot_chart(df, stock_id):
    """
    畫出雙軸折線圖
    左Y軸：ROE、g
    右Y軸：自由現金流
    所有文字標題以英文顯示
    """

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 左邊Y軸：ROE 和 g
    ax1.set_xlabel('Year')
    ax1.set_ylabel('ROE / g (%)', color='black')
    ax1.plot(df['Year'], df['ROE'], color='blue', marker='o', label='ROE')
    ax1.plot(df['Year'], df['g'], color='green', marker='o', label='g')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.legend(loc='upper left')

    # 右邊Y軸：FCF
    ax2 = ax1.twinx()
    ax2.set_ylabel('Free Cash Flow', color='black')
    ax2.plot(df['Year'], df['FCF'], color='red', marker='o', label='FCF')
    ax2.tick_params(axis='y', labelcolor='black')
    ax2.legend(loc='upper right')

    plt.title(f'{stock_id} - ROE, g, and Free Cash Flow (5-year Trend)', fontsize=14)
    plt.tight_layout()

    return fig
