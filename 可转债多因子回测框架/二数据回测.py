import pandas as pd

'''
这里查看下现在的数据全不全
然后对数据进行合并
'''
pd.set_option('expand_frame_repr', False)

df: pd.DataFrame = pd.read_pickle('/Users/lishuai/quant/quant-code/data/all_data_20190910-20220930.pickle')
print(df)

# 任何原始数据读入都进行一下排序、去重，以防万一
df.sort_values(by=['日期', '转债代码'], ascending=[True, True], inplace=True)
df.drop_duplicates(subset=['日期', '转债代码'], inplace=True)
df.reset_index(inplace=True, drop=True)

# 因子数据计算
strategy = {
    "buy_count": 10,  # 只有几股
    "factors": [
        ('转债价格', 1, True),  # 因子名称/权重/大值是否排在首位(从大到小排列)
        ('转股溢价率', 1, True)
    ]
}

# 当天排名计算
# 按照天进行分组,获取本组的因子的个个排名,并将排名按照权重累加,算出来每天的中排名
for factor_name, weight, if_reverse in strategy['factors']:
    df[f'{factor_name}_rank'] = df[factor_name].groupby(df['日期']).rank(ascending=if_reverse, method='first')
# 计算总排名
for factor_name, weight in strategy['factors']:
    df['总排名积分'] = df['总排名积分'] + df[f'{factor_name}_rank'] * weight
df['总排名'] = df['总排名积分'].groupby(df['日期']).rank(ascending=True, method='first')

# 交易信号

# 持仓信号

# 策略评价
