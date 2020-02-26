#-*- coding: utf-8 -*-

# exam.csv

import sys
import math
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
        print(tup[0]*tup[1]*tup[2]*tup[3]*2/1024.)

print("==================== Filter ======================")
filter_dims = data["Filter"].tolist()
print(filter_dims)
for i in filter_dims:
    if not pd.isna(i):
        tup = [int(i) for i in i.split(',')]
        print(tup[0]*tup[1]*tup[2]*tup[3]*2/1024.)

print("==================== Output ======================")
out_dims = data["Output"].tolist()
print(out_dims)
for i in out_dims:
    if not pd.isna(i):
        tup = [int(i) for i in i.split(',')]
        print(tup[0]*tup[1]*tup[2]*tup[3]*2/1024.)

# geo mean
xs = [0.87416137,
0.77186195,
0.80974567,
0.93365728,
0.72258,
0.7618137,
0.961368,
0.8317463,
0.921613,
1.126137,
0.861067,
0.721967,
0.92184619,
1.0318177,
0.9711345,
0.8613613,
0.8901861,
0.850456,
0.95776905,
0.92106137,
0.90619613,
0.880914327]
print(math.exp(math.fsum(math.log(x) for x in xs) / len(xs)))
