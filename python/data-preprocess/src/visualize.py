#!/usr/bin/env python
'''
Raw CSV data visualization.
'''

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
plt.style.use('ggplot')

import seaborn as sns
color = sns.color_palette()
sns.set(rc={'figure.figsize':(25,15)})
import plotly
# connected=True means it will download the latest version of plotly javascript library.
plotly.offline.init_notebook_mode(connected=True)

import plotly.graph_objs as go
import plotly.figure_factory as ff
import cufflinks as cf
import warnings
warnings.filterwarnings('ignore')

# 1. load CSV data
df = pd.read_csv('../data/googleplaystore.csv')
print(df.head())
print("CSV data shape:", df.shape)
#print(df)
#print(df.dtypes)
#df.loc[df.App=='Tiny Scanner - PDF Scanner App']
#df[df.duplicated(keep='first')]
df.drop_duplicates(subset='App', inplace=True)
df = df[df['Android Ver'] != np.nan]
df = df[df['Android Ver'] != 'NaN']
df = df[df['Installs'] != 'Free']
df = df[df['Installs'] != 'Paid']

print('Number of apps in the dataset : ' , len(df))
print(df.sample(7))

# 2. Data Cleaning
# Convert all review text to English language using Google Translator library
# Remove '+' from 'Number of Installs' to make it numeric
df['Installs'] = df['Installs'].apply(lambda x: x.replace('+', '') if '+' in str(x) else x)
df['Installs'] = df['Installs'].apply(lambda x: x.replace(',', '') if ',' in str(x) else x)
df['Installs'] = df['Installs'].apply(lambda x: int(x))
print(type(df['Installs'].values))
df['Installs'] = df['Installs'].apply(lambda x: float(x))
df['Installs'].plot()

# Convert all app sizes to MB
# - Size : Remove 'M', Replace 'k' and divide by 10^-3
#df['Size'] = df['Size'].fillna(0)
df['Size'] = df['Size'].apply(lambda x: str(x).replace('Varies with device', 'NaN') if 'Varies with device' in str(x) else x)
df['Size'] = df['Size'].apply(lambda x: str(x).replace('M', '') if 'M' in str(x) else x)
df['Size'] = df['Size'].apply(lambda x: str(x).replace(',', '') if 'M' in str(x) else x)
df['Size'] = df['Size'].apply(lambda x: float(str(x).replace('k', '')) / 1000 if 'k' in str(x) else x)
df['Size'] = df['Size'].apply(lambda x: float(x))

# Remove '$' from Price
df['Price'] = df['Price'].apply(lambda x: str(x).replace('$', '') if '$' in str(x) else str(x))
df['Price'] = df['Price'].apply(lambda x: float(x))

df['Reviews'] = df['Reviews'].apply(lambda x: int(x))
print(len(df['App']))
#df['Reviews'] = df['Reviews'].apply(lambda x: 'NaN' if int(x) == 0 else int(x))
#print(df.loc[df.Size == 0.713]) #index = 3384
#df.loc[df.col1 == '']['col2']

# 0 - Free, 1 - Paid
# df['Type'] = pd.factorize(df['Type'])[0]
#print(df.dtypes)

print(df.dtypes)
# Data visualization
# This is the basic exploratory analysis to look for any evident patterns or relationships between the features.
rating = df['Rating'].dropna()
df['Rating'].hist()
app_size = df['Size'].dropna()
installs = df['Installs'][df.Installs!=0].dropna() # Install log level
reviews = df['Reviews'][df.Reviews!=0].dropna() # Reviews log10 level
app_type = df['Type'].dropna() # free or paid
#category = df['Category'].dropna()
price = df['Price']
p = sns.pairplot(pd.DataFrame(list(zip(rating, app_size, np.log(installs), np.log10(reviews), app_type, price)), columns=['Rating','Size', 'Installs', 'Reviews', 'Type', 'Price']), hue='Type', palette="Set2")
p = sns.pairplot(pd.DataFrame(list(zip(rating, np.log(installs), np.log10(reviews), app_type, price)), columns=['Rating', 'Installs', 'Reviews', 'Type', 'Price']), hue='Type', palette="Set2")
p = sns.pairplot(pd.DataFrame(list(zip(rating, np.log(installs), np.log10(reviews), app_type)), columns=['Rating', 'Installs', 'Reviews', 'Type']), hue='Type', palette="Set2")
# rating, price and type
p = sns.pairplot(pd.DataFrame(list(zip(np.log(installs), app_type)), columns=['Installs', 'Type']), hue='Type', palette="Set2")
#p = sns.relplot(pd.DataFrame(list(zip(np.log(installs), app_type)), columns=['Installs', 'Type']), hue='Type', palette="Set2")
# rating, price and type
p = sns.pairplot(pd.DataFrame(list(zip(rating, app_type, price)), columns=['Rating', 'Type', 'Price']), hue='Type', palette="Set2")
#plt.show()
#p = sns.pairplot(pd.DataFrame(list(zip(rating, app_size, np.log(installs), np.log10(reviews), category, price)), columns=['Rating','Size', 'Installs', 'Reviews', 'Category', 'Price']), hue='Category')
#p = sns.pairplot(pd.DataFrame(list(zip(rating, app_size, np.log(installs), np.log10(reviews), category, price)), columns=['Rating','Size', 'Installs', 'Reviews', 'Category', 'Price']), hue='Category')

# Which category has the highest share of (active) apps in the market?
number_of_apps_in_category = df['Category'].value_counts().sort_values(ascending=True)
data = [go.Pie(
        labels = number_of_apps_in_category.index,
        values = number_of_apps_in_category.values,
        hoverinfo = 'label+value'

)]

#plotly.offline.iplot(data, filename='active_category')
# TODO: draw with seaborn
# REF: https://blog.algorexhealth.com/2018/03/almost-10-pie-charts-in-10-python-libraries
#p = sns.pairplot(pd.DataFrame(data), hue='Type', palette="Set2")
#plt.show()
# Family and Game apps have the highest market prevelance.
# Interestingly, Tools, Business and Medical apps are also catching up.

# Average rating of apps
# Do any apps perform really good or really bad?
data = [go.Histogram(
        x = df.Rating,
        xbins = {'start': 1, 'size': 0.1, 'end' :5}
)]
print('Average app rating = ', np.mean(df['Rating']))
# Generally, most apps do well with an average rating of 4.17
# Let's break this down and inspect if we have categories which perform exceptionally good or bad
# TODO: draw with seaborn
#plotly.offline.iplot(data, filename='overall_rating_distribution')
#plt.show()

# App ratings across categories - One Way Anova Test
import scipy.stats as stats
f = stats.f_oneway(df.loc[df.Category == 'BUSINESS']['Rating'].dropna(),
               df.loc[df.Category == 'FAMILY']['Rating'].dropna(),
               df.loc[df.Category == 'GAME']['Rating'].dropna(),
               df.loc[df.Category == 'PERSONALIZATION']['Rating'].dropna(),
               df.loc[df.Category == 'LIFESTYLE']['Rating'].dropna(),
               df.loc[df.Category == 'FINANCE']['Rating'].dropna(),
               df.loc[df.Category == 'EDUCATION']['Rating'].dropna(),
               df.loc[df.Category == 'MEDICAL']['Rating'].dropna(),
               df.loc[df.Category == 'TOOLS']['Rating'].dropna(),
               df.loc[df.Category == 'PRODUCTIVITY']['Rating'].dropna()
              )

print(f)
# F_onewayResult(statistic=12.79263715618054, pvalue=2.323280446259348e-20)
print('\nThe p-value is extremely small, hence we reject the null hypothesis in favor of the alternate hypothesis.\n')
#temp = df.loc[df.Category.isin(['BUSINESS', 'DATING'])]
# We can see that the average app ratings across categories is significantly different

# Best performing categories
groups = df.groupby('Category').filter(lambda x: len(x) > 286).reset_index()
array = groups['Rating'].hist(by=groups['Category'], sharex=True, figsize=(20,20))
# The average app ratings across categories is significantly different

groups = df.groupby('Category').filter(lambda x: len(x) >= 170).reset_index()
#print(type(groups.item.['BUSINESS']))
print('Average rating = ', np.nanmean(list(groups.Rating)))
# Average rating =  4.170026786973072
#print(len(groups.loc[df.Category == 'DATING']))
c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 720, len(set(groups.Category)))]
#df_sorted = df.groupby('Category').agg({'Rating':'median'}).reset_index().sort_values(by='Rating', ascending=False)
#print(df_sorted)
layout = {'title' : 'App ratings across major categories',
        'xaxis': {'tickangle':-40},
        'yaxis': {'title': 'Rating'},
          'plot_bgcolor': 'rgb(250,250,250)',
          'shapes': [{
              'type' :'line',
              'x0': -.5,
              'y0': np.nanmean(list(groups.Rating)),
              'x1': 19,
              'y1': np.nanmean(list(groups.Rating)),
              'line': { 'dash': 'dashdot'}
          }]
          }

data = [{
    'y': df.loc[df.Category==category]['Rating'],
    'type':'violin',
    'name' : category,
    'showlegend':False,
    #'marker': {'color': 'Set2'},
    } for i,category in enumerate(list(set(groups.Category)))]
#plotly.offline.iplot({'data': data, 'layout': layout})

# Almost all app categories perform decently. Health and Fitness and Books and Reference produce the highest quality apps with 50% apps having a rating greater than 4.5. This is extremely high!
# On the contrary, 50% of apps in the Dating category have a rating lesser than the average rating.
# A few junk apps also exist in the Lifestyle, Family and Finance category.

# Sizing Strategy - Light Vs Bulky?
# How do app sizes impact the app rating?
groups = df.groupby('Category').filter(lambda x: len(x) >= 50).reset_index()
# sns.set_style('ticks')
# fig, ax = plt.subplots()
# fig.set_size_inches(8, 8)
sns.set_style("darkgrid")
ax = sns.jointplot(df['Size'], df['Rating'])
ax = sns.jointplot(df['Installs'], df['Rating'])
# We can see that most top rated apps are optimally sized between ~2MB to ~40MB - neither too light nor too heavy.
#plt.show()

c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, len(list(set(groups.Category))))]
subset_df = df[df.Size > 40]
groups_temp = subset_df.groupby('Category').filter(lambda x: len(x) >20)

# for category in enumerate(list(set(groups_temp.Category))):
#     print (category)
data = [{
    'x': groups_temp.loc[subset_df.Category==category[1]]['Rating'],
    'type':'scatter',
    'y' : subset_df['Size'],
    'name' : str(category[1]),
    'mode' : 'markers',
    'showlegend': True,
    #'marker': {'color':c[i]}
    #'text' : df['rating'],
    } for category in enumerate(['GAME', 'FAMILY'])]

layout = {'title':"Rating vs Size",
          'xaxis': {'title' : 'Rating'},
          'yaxis' : {'title' : 'Size (in MB)'},
         'plot_bgcolor': 'rgb(0,0,0)'}

plotly.offline.iplot({'data': data, 'layout': layout})

# heavy_categories = [ 'ENTERTAINMENT', 'MEDICAL', 'DATING']
# data = [{
#     'x': groups.loc[df.Category==category]['Rating'],
#     'type':'scatter',
#     'y' : df['Size'],
#     'name' : category,
#     'mode' : 'markers',
#     'showlegend': True,
#     #'text' : df['rating'],
#     } for category in heavy_categories]

# We can see that most bulky apps ( >50MB) belong to the Game and Family category. Despite this, these bulky apps are fairly highly rated indicating that they are bulky for a purpose.

# Pricing Strategy - Free Vs Paid?
paid_apps = df[df.Price>0]
p = sns.jointplot( "Price", "Rating", paid_apps)
#plt.show()
# We can see that most top rated apps are optimally priced between ~1$ to ~30$. There are only a very few apps priced above 20$.

# Current pricing trend - How to price your app?
subset_df = df[df.Category.isin(['GAME', 'FAMILY', 'PHOTOGRAPHY', 'MEDICAL', 'TOOLS', 'FINANCE',
                                 'LIFESTYLE','BUSINESS'])]
sns.set_style('darkgrid')
fig, ax = plt.subplots()
fig.set_size_inches(15, 8)
#p = sns.stripplot(x="Price", y="Category", data=subset_df, jitter=True, linewidth=1)
p = sns.stripplot(x="Installs", y="Category", data=subset_df, jitter=True, linewidth=1)
title = ax.set_title('App installation trend across categories')
#plt.show()
#Shocking...Apps priced above 250$ !!! Let's quickly examine what these junk apps are.
#print('Junk apps priced above 350$')
print(df[['Category', 'App']][df.Price > 200])

fig, ax = plt.subplots()
fig.set_size_inches(15, 8)
subset_df_price = subset_df[subset_df.Price<100]
p = sns.stripplot(x="Price", y="Category", data=subset_df_price, jitter=True, linewidth=1)
title = ax.set_title('App pricing trend across categories - after filtering for junk apps')
#plt.show()
# We can see that:
# Clearly, Medical and Family apps are the most expensive. Some medical apps extend even upto 80$.
# All other apps are priced under 30$.
# Surprisingly, all game apps are reasonably priced below 20$.

# Distribution of paid and free apps across categories
# Stacked bar graph for top 5-10 categories - Ratio of paid and free apps
#fig, ax = plt.subplots(figsize=(15,10))

new_df = df.groupby(['Category', 'Type']).agg({'App' : 'count'}).reset_index()
#print(new_df)

# outer_group_names = df['Category'].sort_values().value_counts()[:5].index
# outer_group_values = df['Category'].sort_values().value_counts()[:5].values

outer_group_names = ['GAME', 'FAMILY', 'MEDICAL', 'TOOLS']
outer_group_values = [len(df.App[df.Category == category]) for category in outer_group_names]

a, b, c, d=[plt.cm.Blues, plt.cm.Reds, plt.cm.Greens, plt.cm.Purples]


inner_group_names = ['Paid', 'Free'] * 4
inner_group_values = []
#inner_colors = ['#58a27c','#FFD433']


for category in outer_group_names:
    for t in ['Paid', 'Free']:
        x = new_df[new_df.Category == category]
        try:
            #print(x.App[x.Type == t].values[0])
            inner_group_values.append(int(x.App[x.Type == t].values[0]))
        except:
            #print(x.App[x.Type == t].values[0])
            inner_group_values.append(0)

explode = (0.025,0.025,0.025,0.025)
# First Ring (outside)
fig, ax = plt.subplots(figsize=(10,10))
ax.axis('equal')
mypie, texts, _ = ax.pie(outer_group_values, radius=1.2, labels=outer_group_names, autopct='%1.1f%%', pctdistance=1.1,
                                 labeldistance= 0.75,  explode = explode, colors=[a(0.6), b(0.6), c(0.6), d(0.6)], textprops={'fontsize': 16})
plt.setp( mypie, width=0.5, edgecolor='black')

# Second Ring (Inside)
mypie2, _ = ax.pie(inner_group_values, radius=1.2-0.5, labels=inner_group_names, labeldistance= 0.7,
                   textprops={'fontsize': 12}, colors = [a(0.4), a(0.2), b(0.4), b(0.2), c(0.4), c(0.2), d(0.4), d(0.2)])
plt.setp( mypie2, width=0.5, edgecolor='black')
plt.margins(0,0)
plt.show()
