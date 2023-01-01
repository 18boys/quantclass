import pandas as pd

df = pd.read_csv('./data/all_date.csv')
df = df.set_index(['日期'])
df.to_csv(f'./data/all_date.csv')

