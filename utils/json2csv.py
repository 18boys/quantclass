import json
# import pandas as pd
fs = open('/Users/lishuai/quant/quant-code/可转债/data/可转债行情数据(20190101-20221229).json','r',encoding='utf8')
json_obj = json.load(fs)


fs_write = open('../data/可转债行情数据(20190101-20221229).csv', 'w', encoding='utf8')
# 这里需要去掉开头和结尾的引号
fs_write.write(json_obj['content'])

