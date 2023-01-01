import pandas as pd
import xlrd  # pip install xlrd==1.2.0 需要写死版本
import os


xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True

excelPath = '/Users/lishuai/quant/可转债数据存放/购买数据2'
file_list = os.listdir(excelPath)
# file_list = os.walk(excelPath)
# print([file for file in file_list ])
file_list.sort()
file_list = list(filter(lambda x: 'xlsx' in x, file_list))
print(file_list)
print(len(file_list))

alldata = pd.DataFrame()
for i in range(len(file_list)):
    path = f'{excelPath}/{file_list[i]}'
    wb = xlrd.open_workbook(path)
    sheets = wb.sheet_names()
    print(f'开始处理第{i}个')
    for j in range(len(sheets)):
        df = pd.read_excel(path, sheet_name=j, index_col=None, skipfooter=4)
        del df['序号']
        df['日期'] = sheets[j]
        df = df.set_index(['日期'])
        alldata = pd.concat([alldata, df])
alldata.to_csv('./merge_data_2.csv')

# excels = [pd.read_excel(f'{excelPath}/{fName}') for fName in file_list]
# df = pd.concat(excels)
# df.to_excel('汇总.xlsx', index=False)
# exit()

# excel_name = './ninwin_cb_data_202209.xlsx'
# wb = xlrd.open_workbook(excel_name)
#
# # 获取workbook中所有的sheet
# sheets = wb.sheet_names()
# print(sheets)
#
# alldata = pd.DataFrame()
# for i in range(len(sheets)):
#     df = pd.read_excel(excel_name, sheet_name=i, index_col=None, skipfooter=4)
#     del df['序号']
#     df['日期'] = sheets[i]
#     df = df.set_index(['日期'])
#     alldata = pd.concat([alldata, df])
# alldata.to_csv('./merge_data.csv')
