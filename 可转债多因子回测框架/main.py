import pandas as pd

'''
这里查看下现在的数据全不全
然后对数据进行合并
'''
pd.set_option('expand_frame_repr', False)

df = pd.read_pickle('/Users/lishuai/quant/quant-code/可转债/data/20192021可转债data.pkl')
df_merge = pd.read_csv('/Users/lishuai/quant/quant-code/可转债/data/merge_data.csv')
print(df)