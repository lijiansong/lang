import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

'''
Note: Excel filter for my girl friend :-)
'''
def excel_filter(excel_file_path, sheet_name, column_name, new_excel_name):
    df = pd.read_excel(excel_file_path, sheetname=sheet_name)
    print("Column headings:")
    print(df.columns)
    target_columns = []
    for i, v in enumerate(df[column_name]):
        target_columns.append((i, float(v)))
    # <index, value> pairs, sort by values
    target_columns = sorted(target_columns, key=lambda item: item[1])
    print(target_columns)
    i = 0
    j = len(target_columns) - 1
    to_delete_indices_list = []
    while(target_columns[i][1] <= 0):
        if target_columns[i][1] + target_columns[j][1] == 0:
            to_delete_indices_list.append(target_columns[i][0])
            to_delete_indices_list.append(target_columns[j][0])
            i += 1
            j -= 1
        elif abs(target_columns[i][1]) > abs(target_columns[j][1]):
            i += 1
        else:
            # abs(target_columns[i][1]) < abs(target_columns[j][1])
            j -= 1
    print(to_delete_indices_list)
    df = df.drop(to_delete_indices_list)
    writer = ExcelWriter(new_excel_name)
    df.to_excel(writer, sheet_name, index=False)
    writer.save()

if __name__ == '__main__':
    '''
    col_name = '借方金额(本位币)'
    sheet_name = 'Sheet1'
    excel_name = 'a.xlsx'
    new_excel_name = 'a-new.xlsx'
    excel_filter(excel_name, sheet_name, col_name, new_excel_name)
    '''
    col_name = 'net'
    sheet_name = '物流'
    excel_name = '26400.01-4 细节测试-劳务支出-物流(26-02-2020 10.48.07 AM).xlsx'
    new_excel_name = 'a-new.xlsx'
    excel_filter(excel_name, sheet_name, col_name, new_excel_name)
