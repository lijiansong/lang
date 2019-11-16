import pandas as pd
import numpy as np

def get_pc_table(url):
    tables = pd.read_html(url)
    return tables[0]

if __name__ == '__main__':
    cgo20_url = r'https://cgo20.hotcrp.com/users?t=pc'
    cgo20_pc_table = get_pc_table(cgo20_url)
    print(type(cgo20_pc_table))
    print(type(cgo20_pc_table.values))
    #print(cgo20_pc_table)
    pldi20_url = r'https://pldi2020.hotcrp.com/users?t=pc'
    pldi20_pc_table = get_pc_table(pldi20_url)
    #print(pldi20_pc_table)
    pc_inter = np.intersect1d(cgo20_pc_table.values[:, 0], pldi20_pc_table.values[:, 0])
    print(pc_inter)
    pc_dict = {}
    for item in cgo20_pc_table.values:
        pc_dict[item[0]] = item[1]
    for i in pc_inter:
        print(i, ': ', pc_dict[i])

