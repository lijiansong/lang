#!/usr/bin/env python
'''
CSV data visualization.
'''

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
#plt.style.use('ggplot')



# 1. load CSV data
df = pd.read_csv('data.csv')
print("CSV data shape:", df.shape)
print(df['Category'])
print(df['Number'])

# Remove '+' from 'Number' to make it numeric
df['Number'] = df['Number'].apply(lambda x: str(x).replace('+', '') if '+' in str(x) else x)
df['Number'] = df['Number'].apply(lambda x: int(str(x).replace('K', '')) * 1000 if 'K' in str(x) else x)
df['Number'] = df['Number'].apply(lambda x: int(x))
print("After numeric:")
print(df['Number'])

is_dup = df['Category'].value_counts()
print(is_dup.index)
print(is_dup.values)
plt.figure(figsize=(8,4))
color = ['r', 'g', 'b']
ax = sns.barplot(df['Category'], df['Number'], alpha=0.8, color=color[1])
ax.set_xlabel('Category')
ax.set_ylabel('Number of Occurrences')
plt.show()
