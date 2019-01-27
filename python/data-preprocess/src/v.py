#importing required packages
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import numpy as np
warnings.filterwarnings("ignore")
#%matplotlib inline
sns.set(style="whitegrid")
#import missingno as msno
#Interactive
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from IPython.display import display, HTML

#Reading data
storedata = pd.read_csv("../data/googleplaystore.csv")

print("\n First 7 rows in our dataset")
display(storedata.head(7))

print("\n Number of rows in our dataset = " + str(storedata.shape[0]))

#Last Updated to (Month, Year) to number
storedata['Last Updated'] = pd.to_datetime(storedata['Last Updated'],format='%B %d, %Y',errors='coerce').astype('str')

def split_mul(data):
    try:
        data=list(map(int,data.split('-')))
        return data[0]+(data[1]*12)+data[2]
    except:
        return "Nan"
storedata['Last Updated'] = [split_mul(x) for x in storedata['Last Updated']]

#Improve 'Android Ver' and 'Installs' representation
storedata["Android Ver"] = storedata["Android Ver"].str.split(n=1, expand=True)

def deal_with_abnormal_strings(data):
    data[data.str.isnumeric()==False]=-1
    data=data.astype(np.float32)
    return data

storedata.Installs = [x.strip().replace('+', '').replace(',','') for x in storedata.Installs]
storedata.Installs = deal_with_abnormal_strings(storedata.Installs)

storedata.Size = [x.strip().replace('M', '').replace(',','') for x in storedata.Size]

def convert_float(val):
    try:
        return float(val)
    except ValueError:
        try:
            val=val.split('.')
            return float(val[0]+'.'+val[1])
        except:
            return np.nan

storedata.head(7)
#Number of categories of apps in the store.....
def plot_number_category():
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 7)
    fig.autofmt_xdate()
    countplot=sns.categorical.countplot(storedata.Category,ax=ax)
    plt.show(countplot)

plot_number_category()

# Tabular representation
top_cat=storedata.groupby('Category').size().reset_index(name='Count').nlargest(6,'Count')
display(top_cat)

cat=top_cat.Category.tolist()
data_top6=storedata.groupby('Category')['Installs'].agg('sum').loc[cat].reset_index(name='Number_Installations')
data=storedata.groupby('Category')['Installs'].agg('sum').reset_index(name='Number_Installations')

#Comparing top 5 category on the basis of 'Installs'
def compare_6(data):
    fig = plt.figure(figsize=(12,4))
    title=plt.title('Comparing top 5 category on the basis of Installs')
    bar=sns.barplot(x=data['Category'],y=data['Number_Installations'])
    for item in bar.get_xticklabels():
        item.set_rotation(60)
    plt.show(bar)

#Comparing all categoryies on the basis of 'Installs'
def compare_all(data):
    fig = plt.figure(figsize=(12,7))
    title=plt.title('Comparing all categories on the basis of Installs')
    index = data['Category'].value_counts()
    bar=sns.barplot(index.index, index.values)
    bar.set_ylabel('Number of Installs')
    bar.set_xlabel('Category')
    #for item in bar.get_xticklabels():
    #    item.set_rotation(60)
    plt.show(bar)

compare_6(data_top6)
compare_all(data)
