# 引入 `Counter`，用於對上字韻母計數
from collections import Counter
# 引入 `accumulate` 函式，用於輔助計算坐標的位置
from itertools import accumulate
# 引入 `matplotlib`，用於繪圖
# 安裝方法：`pip install matplotlib`
import matplotlib.pyplot as plt
# 引入 `QieyunEncoder`，用於解析切韻音系音韻地位
# 所用 `QieyunEncoder` 版本爲 `0.5.0`
# 安裝方法：`pip install "qieyun-encoder==0.5.0"`
# 由於 `QieyunEncoder` 目前仍處於測試版，使用方法可能會發生變動，
# 因此需要固定版本號
import QieyunEncoder

# 使用思源黑體 傳統 (Source Han Sans Classic) 顯示
# 字體下載地址 https://github.com/redchenjs/source-han-sans-classic
# 亦可在此處更換爲其他字體
# 如果 matplotlib 提示無法找到字體，可以參考 https://stackoverflow.com/a/65179297
plt.rcParams['font.family'] = 'Source Han Sans C'

# 創建 `Counter` 物件，用於計數
d韻到上字頻次 = Counter()

# 開啓廣韻反切音韻地位表
with open('廣韻反切音韻地位表.csv') as f:
    # 跳過第一行，第一行爲標題行，無需解析
    next(f)

    # 對於後續的每一行
    for line in f:
        # 去除行尾的換行符，然後以逗號分開
        小韻號, 小韻首字, 上字, 下字, 被切字音韻描述, 上字音韻描述們, 下字音韻描述們 = line.rstrip('\n').split(',')

        # 由音韻描述建立音韻地位對象
        # 可能有多種可能的音韻地位，以 / 分隔，所以需要轉換爲 list
        上字音韻地位們 = list(map(QieyunEncoder.音韻地位.from描述, 上字音韻描述們.split('/')))

        # 若有多種可能的音韻地位，則每種可能的音韻地位都參與計數
        for 上字音韻地位 in 上字音韻地位們:
            d韻到上字頻次[上字音韻地位.韻] += 1

# 將各韻頻次存儲到 `list` 中
# 各韻的排列順序按照 `QieyunEncoder` 的預設順序
各韻頻次 = [d韻到上字頻次[韻] for 韻 in QieyunEncoder.常量.所有韻]

# 初始化
fig, ax = plt.subplots()

# 計算各坐標的位置
positions = list(accumulate(range(len(QieyunEncoder.常量.所有韻) - 1), lambda x, _: x + 0.75, initial=0.5))

# 繪圖
p1 = ax.bar(positions, 各韻頻次, width=0.5, edgecolor='black', color='#ccc')
ax.axhline(0, color='grey', linewidth=0.8)
ax.set_title('廣韻反切上字韻母統計圖', pad='15', fontsize='x-large', fontweight='bold')
ax.set_xticks(positions)
ax.set_xticklabels(list(QieyunEncoder.常量.所有韻))
ax.bar_label(p1)

# 顯示
plt.show()
