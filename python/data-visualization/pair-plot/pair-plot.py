import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# 1. load CSV data
df = pd.read_csv('./data/dense-fp16-mobilenet.csv')
print(df.head())
print("CSV data shape:", df.shape)
df = df.drop(['fifo size', 'Hardware FPS', 'Total execution time(ms)', 'Prepare input time(ms)', 'Copyin time(ms)', 'Execution time(ms)', 'Copyout time(ms)', 'Post process time(ms)'], axis=1)
# batch size  data parallel  model parallel  thread num  End to end FPS
BS, DP, MP, TN, E2E = 'batch size',  'data parallel',  'model parallel',  'thread num',  'End to end FPS'
df = df.reindex([E2E, TN, DP, MP, BS], axis=1)
print(df.head())

ax = sns.pairplot(df, kind='reg', diag_kind='kde')
plt.xscale('log', basex=2)
plt.yscale('log', basey=2)
plt.show()
