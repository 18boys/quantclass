import pandas as pd

'''
1.将data中宁稳的数据进行合并,并将空的数据去除
'''
pd.set_option('expand_frame_repr', False)

df_source = pd.read_csv('/Users/lishuai/quant/quant-code/可转债/data/merge_data.csv', parse_dates=['日期'])
print(len(df_source))
df_two = pd.read_csv('/Users/lishuai/quant/quant-code/可转债/data/merge_data_2.csv', parse_dates=['日期'])
print(len(df_two))

df_source = pd.concat([df_source, df_two])
# df_source.set_index('日期', inplace=True)
print(len(df_source))

df_target: pd.DataFrame = pd.read_pickle('/Users/lishuai/quant/quant-code/可转债/data/20192021可转债data.pkl')
df_target['日期'] = pd.to_datetime(df_target['base_date'])
del df_target['base_date']
del df_target['Unnamed: 0']
del df_target['序号']
# df_target.set_index('日期', inplace=True)
# df_target = df_target[:, '转债代码':]
print(len(df_target))
df_source = pd.concat([df_source, df_target])
# df_source = pd.merge(df_source,df_target,how='outer', on=['日期', '转债代码'])
df_source.sort_values(by=['日期', '转债代码'], inplace=True)
del df_source['转债名称.1']
del df_source['MA20乖离']
del df_source['热门度']
print(len(df_source))
print(df_source)

# 去掉空行数据
df_source = df_source[df_source['转债代码'].notna()]

# 去重
df_source.drop_duplicates(subset=['日期', '转债代码'], keep='first', inplace=True)

# df_source.to_pickle('ningwen_data_20190910-20220930.pickle')
# df_source.to_csv('ningwen_data_20190910-20220930.csv', index=False)
# df_source.to_hdf('ningwen_data_20190910-20220930.hdf', key='ningweng')

df_dup = df_source[(df_source['日期'] > pd.to_datetime('2021-07-01')) & (df_source['日期'] < pd.to_datetime('2021-09-01'))]
print(df_dup)


