import pandas as pd

pd.set_option('expand_frame_repr', False)

'''
将宁稳网数据与bigquant的行情数据合并
测试例子:
import pandas as pd
left = pd.DataFrame({
   'id':[1,2,3,4],
   'Name': ['Smith', 'Maiki', 'Hunter', 'Hilen'],
   'subject_id':['sub1','sub2','sub4','sub6']})
right = pd.DataFrame({
    'idAlias':[1,2,3,4,5],
    'NameAlias': ['Smith', 'Maiki111', 'Hunter', 'Hilen', 'hehe'],
    'subject_name':['name1','name2','name3','name4', 'name5']})
print(pd.merge(left,right,left_on=['id','Name'],right_on=['idAlias','NameAlias'], how='left'))

'''
ROOT = '/Users/lishuai/quant/quant-code/'
df_market = pd.read_csv(f'{ROOT}/data/可转债行情数据(20190101-20221229).csv', parse_dates=['date'])
del df_market['Unnamed: 0']
df_nw = pd.read_pickle(f'{ROOT}/data/ningwen_data_20190910-20220930.pickle')
df_nw['转债代码'] = df_nw['转债代码'].astype(int)
df_nw['股票代码'] = df_nw['股票代码'].astype(int)
print(df_market)
print(df_nw)
df = pd.merge(df_nw, df_market, left_on=['日期', '转债代码'],right_on=['date', 'instrument'])
df.to_pickle('all_data_20190910-20220930.pickle')

