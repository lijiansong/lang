import pandas as pd
import numpy as np

def get_pc_table(url):
    tables = pd.read_html(url)
    return tables[0]

def extract_pc_table(pc_file_name):
    pc_list = []
    with open(pc_file_name, 'r') as f:
        pc_info = f.readlines()
        for pc in pc_info:
            pc_list.append(pc.split(',')[0])
    return pc_list

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

    print('===----------------- PACT\'20 -----------------===')
    pact20_url = r'https://pact2020submission.cc.gatech.edu/users.php?t=pc'
    pact20_pc_table = get_pc_table(pact20_url)
    pact20_pc_set = set(pact20_pc_table['Name'])
    print(pact20_pc_set)

    print('===----------------- MASCOTS\'20 -----------------===')
    mascots20_pc_list = extract_pc_table('mascots20-pc.txt')
    mascots20_pc_set = set(mascots20_pc_list)
    print(mascots20_pc_set)

    print('===----------------- PACT\'20 & MASCOTS\'20 -----------------===')
    print(pact20_pc_set & mascots20_pc_set)
