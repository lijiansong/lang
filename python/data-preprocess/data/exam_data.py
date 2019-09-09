#-*- coding: utf-8 -*-

# exam.csv

import sys
import pandas as pd

input_file = sys.argv[1]

data = pd.read_csv(input_file, delimiter='#')
print (data)

data["Name"] = data["Name"].apply(lambda s: s.lower())
#data["Name"].to_csv("exam.csv", encoding="utf-8", index=False)
bench_names = data["Name"].tolist()
print(bench_names)

print("==================== Input ======================")
input_dims = data["Input"].tolist()
print(input_dims)
for i in input_dims:
    if not pd.isna(i):
        tup = [int(i) for i in i.split(',')]
        print(tup[0]*tup[1]*tup[2]*tup[3]*2/1024)

print("==================== Filter ======================")
filter_dims = data["Filter"].tolist()
print(filter_dims)
for i in filter_dims:
    if not pd.isna(i):
        tup = [int(i) for i in i.split(',')]
        print(tup[0]*tup[1]*tup[2]*tup[3]*2/1024)

print("==================== Output ======================")
out_dims = data["Output"].tolist()
print(out_dims)
for i in out_dims:
    if not pd.isna(i):
        tup = [int(i) for i in i.split(',')]
        print(tup[0]*tup[1]*tup[2]*tup[3]*2/1024)
