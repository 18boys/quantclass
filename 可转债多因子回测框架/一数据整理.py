import pandas as pd

'''
1.三个部分收集到的宁稳网数据进行合并
'''
pd.set_option('expand_frame_repr', False)

# 宁稳网202109-202209数据
df_source = pd.read_csv('/Users/lishuai/quant/quant-code/data/merge_data.csv', parse_dates=['日期'])
print(len(df_source))
# 宁稳网202107-202108数据
df_two = pd.read_csv('/Users/lishuai/quant/quant-code/data/merge_data_2.csv', parse_dates=['日期'])
print(len(df_two))

df_source = pd.concat([df_source, df_two])
print(len(df_source))
df_source['股票涨跌'] = df_source['涨跌.1']
# df_source['税前收益率'] = df_source['税前收益率'].apply(lambda x: float(x.strip('%')) / 100 if (('%' in x) & ('<' not in x) & ('>' not in x)) else x)
df_source['转股溢价率'] = df_source['转股溢价率']/100
df_source['税前收益率'] = df_source['税前收益率'].apply(lambda x: float(x.strip('%')) / 100 if (('%' in str(x)) & ('<' not in str(x)) & ('>' not in str(x))) else x)
df_source['税后收益率'] = df_source['税后收益率'].apply(lambda x: float(x.strip('%')) / 100 if (('%' in str(x)) & ('<' not in str(x)) & ('>' not in str(x))) else x)
df_source['税前回售收益'] = df_source['税前回售收益'].apply(lambda x: float(x.strip('%')) / 100 if (('%' in str(x)) & ('<' not in str(x)) & ('>' not in str(x))) else x)
df_source['税后回售收益'] = df_source['税后回售收益'].apply(lambda x: float(x.strip('%')) / 100 if (('%' in str(x)) & ('<' not in str(x)) & ('>' not in str(x))) else x)

del df_source['涨跌.1']
del df_source['老式排名']
del df_source['老式双低']
del df_source['新式双低']
del df_source['新式排名']
del df_source['热门度']


# 网上找到201909-20210706数据
df_target: pd.DataFrame = pd.read_pickle('/Users/lishuai/quant/quant-code/data/20192021可转债data.pkl')
df_target['日期'] = pd.to_datetime(df_target['base_date'])
df_target['股票涨跌'] = df_target['涨跌.1']
del df_target['涨跌.1']
del df_target['base_date']
del df_target['Unnamed: 0']
del df_target['序号']
del df_target['老式排名']
del df_target['老式双低']
del df_target['新式双低']
del df_target['新式排名']
del df_target['热门度']
del df_target['转债名称.1']

df_target['涨跌'] = df_target['涨跌'].str.strip('%').astype(float)/100
df_target['转股溢价率'] = df_target['转股溢价率'].str.strip('%').astype(float)/100
df_target['转债换手率'] = df_target['转债换手率'].str.strip('%').astype(float)/100
df_target['余额/市值'] = df_target['余额/市值'].str.strip('%').astype(float)/100
df_target['余额/股本'] = df_target['余额/股本'].str.strip('%').astype(float)/100
df_target['税前收益率'] = df_target['税前收益率'].str.strip('%').astype(float)/100
df_target['税后收益率'] = df_target['税后收益率'].str.strip('%').astype(float)/100

df_target['税前回售收益'] = df_target['税前回售收益'].apply(lambda x: float(x.strip('%')) / 100 if '%' in x else x)
df_target['税后回售收益'] = df_target['税后回售收益'].apply(lambda x: float(x.strip('%')) / 100 if '%' in x else x)


print(len(df_target))
df_source = pd.concat([df_source, df_target])
df_source.sort_values(by=['日期', '转债代码'], inplace=True)

# 去掉空行数据
df_source = df_source[df_source['转债代码'].notna()]

# 去重
df_source.drop_duplicates(subset=['日期', '转债代码'], keep='first', inplace=True)
df_source['转债代码'] = df_source['转债代码'].astype(int)
df_source['股票代码'] = df_source['股票代码'].astype(int)

# df_dup = df_source[(df_source['日期'] > pd.to_datetime('2021-07-01')) & (df_source['日期'] < pd.to_datetime('2021-09-01'))]
# print(df_dup)

ROOT = '/Users/lishuai/quant/quant-code/'
df_market = pd.read_csv(f'{ROOT}/data/可转债行情数据(20190101-20221229).csv', parse_dates=['date'])
del df_market['Unnamed: 0']

df = pd.merge(df_source, df_market, left_on=['日期', '转债代码'], right_on=['date', 'instrument'])
df.to_pickle(f'{ROOT}/data/all_data_20190910-20220930.pickle')
