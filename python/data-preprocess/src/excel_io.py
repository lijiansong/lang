
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

'''
Notice: If you're using python3, then install:
    pip3 install xlsxwriter
'''

# OrderedDict is better.
df = pd.DataFrame({'1a':[1,3,5,7,4,5,6,4,7,8,9],
                   '0a':[3,5,6,2,4,6,7,8,7,8,9]})

writer = ExcelWriter('Pandas-Example.xlsx')
df.to_excel(writer,'Sheet1-name',index=False)
df.to_excel(writer,'Sheet2-name',index=False)
writer.save()
