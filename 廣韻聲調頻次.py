# 引入 `Counter`，用於對上字聲調計數
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
d聲到字頭頻次 = Counter()

# 開啓廣韻表
# 由於廣韻表格式未來可能發生變動，使用時需要固定版本號
# 所用版本爲 https://raw.githubusercontent.com/nk2028/qieyun-data/9675d039f953393e248212354ea764eb3aad8dc3/%E9%9F%BB%E6%9B%B8/%E5%BB%A3%E9%9F%BB.csv
with open('廣韻.csv') as f:
    # 跳過第一行，第一行爲標題行，無需解析
    next(f)

    # 對於後續的每一行
    for line in f:
        # 去除行尾的換行符，然後以逗號分開
        小韻號, 韻部原貌, 最簡描述, 反切覈校前, 反切, 字頭覈校前, 字頭, 釋義, 釋義補充, 圖片id = line.rstrip('\n').split(',')

        # 由音韻描述構造音韻地位物件
        當前音韻地位 = QieyunEncoder.音韻地位.from描述(最簡描述)

        # 計數
        d聲到字頭頻次[當前音韻地位.聲] += 1

# 將各聲頻次存儲到 `list` 中
# 各聲的排列順序按照 `QieyunEncoder` 的預設順序
各聲頻次 = [d聲到字頭頻次[聲] for 聲 in QieyunEncoder.常量.所有聲]

# 初始化
fig, ax = plt.subplots()

# 計算各坐標的位置
positions = list(accumulate(range(len(QieyunEncoder.常量.所有聲) - 1), lambda x, _: x + 0.5, initial=0.5))

# 繪圖
p1 = ax.bar(positions, 各聲頻次, width=0.25, edgecolor='black', color='#ccc')
ax.axhline(0, color='grey', linewidth=0.8)
ax.set_title('廣韻各聲調字數統計圖', pad='15', fontsize='x-large', fontweight='bold')
ax.set_xticks(positions)
ax.set_xticklabels(list(QieyunEncoder.常量.所有聲))
ax.bar_label(p1)

# 顯示
plt.show()
