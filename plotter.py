# 左邊Y軸：ROE 和 g
ax1.set_xlabel('Year')
ax1.set_ylabel('ROE / g (%)', color='black')
ax1.plot(df['Year'], df['ROE'], color='blue', marker='o', label='ROE')
ax1.plot(df['Year'], df['g'], color='green', marker='o', label='g')
ax1.tick_params(axis='y', labelcolor='black')

# ➜ 加上數字標籤
for x, y in zip(df['Year'], df['ROE']):
    ax1.text(x, y, f'{y:.1f}', color='blue', fontsize=8, ha='center', va='bottom')

for x, y in zip(df['Year'], df['g']):
    ax1.text(x, y, f'{y:.1f}', color='green', fontsize=8, ha='center', va='bottom')

ax1.legend(loc='upper left')

# 右邊Y軸：FCF
ax2 = ax1.twinx()
ax2.set_ylabel('Free Cash Flow', color='black')
ax2.plot(df['Year'], df['FCF'], color='red', marker='o', label='FCF')
ax2.tick_params(axis='y', labelcolor='black')

# ➜ 加上數字標籤
for x, y in zip(df['Year'], df['FCF']):
    ax2.text(x, y, f'{y:.0f}', color='red', fontsize=8, ha='center', va='bottom')

ax2.legend(loc='upper right')
