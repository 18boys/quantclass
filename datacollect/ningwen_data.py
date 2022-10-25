import pandas as pd
from datetime import datetime

# 每次手动执行curl，将今天的数据下载到本地，然后再执行处理命令
# 每次得到最新的结果之后，注意将数据备份
# 数据不放在工程中，电脑其他地方备份一份，网盘上一份，保证数据不丢失

df = pd.read_html(
    './index.html',
    attrs={
        'id': 'cb_hq'
    },
)[0]

df = pd.DataFrame(df)
del df['转债名称.1']
del df['序号']
#
# now = datetime.now()
# dataStr = now.strftime('%Y-%m-%d')
dataStr = '2022-10-24'
df['日期'] = dataStr
print(df)

# 备份今日数据
df.to_csv(f'single_date_{dataStr}.csv', mode='a', index=False)
# 写入总表
df.to_csv(f'all_date.csv', mode='a', index=False)
