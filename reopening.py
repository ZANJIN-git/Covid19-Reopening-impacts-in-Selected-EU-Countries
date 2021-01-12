#!/usr/bin/env python
# coding: utf-8




import numpy as np
import pandas as pd
import json
import requests
from urllib.request import urlopen
#from pandas.io.json import json_normalize 
import os 

#Graphing 1

import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
data_path = r"C:\Users\zjin2\Desktop\python\reopening practice\data"

p3 = pd.read_stata((os.path.join(data_path,'_data_p3.dta')))

ddd = pd.Timestamp('2020-06-01')
p3.loc[(p3['sample'] == 1)  & (p3['grp_970']==1),'plot_grp'] = 1
p3.loc[(p3['sample'] == 1)  & (p3['grp_970']!=1),'plot_grp'] = 2
p3.loc[(p3['sample'] != 1),'plot_grp'] = 3
sns.set(style="ticks")
sns.set_context("paper")
plot_data = p3[(p3.date==ddd) & (p3['total_cases_per_million']<4000) 
               & (p3['test_last'].notnull()) & (p3['test_last']<100)]
g=sns.relplot('total_cases_per_million','test_last',data=plot_data,
            hue='plot_grp',palette ='Set1',kind='scatter',alpha=0.6,s=25)
g.set_axis_labels("Total confirmed cases per million", "Total tested per thousands")
g._legend.remove()

def annotation(grp):
  j = [i==grp for i in plot_data['plot_grp']]
  xval = plot_data.loc[j, 'total_cases_per_million']
  yval = plot_data.loc[j, 'test_last']
  text = plot_data.loc[j, 'isocode']
  for x,y,t in zip(xval,yval,text):
    g.axes[0,0].text(x+0.2,y+1,t,horizontalalignment='left', size=10, color='black', weight=None)
annotation(1)
annotation(2)
plt.title("Testing against instensity of outbreak",fontsize=15)



#Graphing 2

country = ['Austria','Denmark','France','China','Germany','Italy','Sweden','South Korea']
plot_data = p3[(p3.country.isin(country)) & (p3['days_peak_c']>=-40) & (p3['days_peak_c']<40)] [['country','ma7_new_cases_per_million','ma7_new_deaths_per_million','days_peak_c','open_r','reopen_r']]
f, axes = plt.subplots(2, 4, figsize=(15, 6))
def draw(cntry,r,c):
    y1=plot_data[plot_data['country']==cntry]['ma7_new_cases_per_million']
    y2=plot_data[plot_data['country']==cntry]['ma7_new_deaths_per_million']
    x=plot_data[plot_data['country']==cntry]['days_peak_c']
    ax = sns.lineplot(x,y1,ax=axes[r, c],color='r',label='Daily cases')
    
    v1_xmin =plot_data[(plot_data['country']==cntry) & (plot_data['open_r']!=0)]['days_peak_c'].min()
    v1_xmax =plot_data[(plot_data['country']==cntry) & (plot_data['open_r']!=0)]['days_peak_c'].max()
    v2_xmin =plot_data[(plot_data['country']==cntry) & (plot_data['reopen_r']!=0)]['days_peak_c'].min()
    v2_xmax =plot_data[(plot_data['country']==cntry) & (plot_data['reopen_r']!=0)]['days_peak_c'].max()
    
    ax.axvspan(v1_xmin, v1_xmax, alpha=0.2, color='red',label='Lockdown')
    ax.axvspan(v2_xmin, v2_xmax, alpha=0.2, color='yellow',label='Reopen')

    ax2 = ax.twinx()
    ax2.plot(x,y2,color='black',label='Daily deaths (RHS)')
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1+h2,l1+l2)
    ax.set_title(cntry,fontsize=12,color='royalblue')
    ax.set_ylabel('')    
    ax.set_xlabel('')
    ax.get_legend().remove()
    #ax.margins(y=0)
    return [h1+h2,l1+l2]

for c,i in zip(country[:4],range(4)):
    a = draw(c,0,i)
for c,i in zip(country[4:],range(4)):
    b = draw(c,1,i)

#h1, l1 = axes[0,0].get_legend_handles_labels()
f.legend(a[0], a[1], loc = 8,ncol=4, bbox_to_anchor=(0.5,-0.02),prop={"size":12},frameon=False)
f.suptitle("COVID-19 Daily Cases and Deaths During Lockdown/Reopening",ha='center',y=1.05,fontsize=16,color='royalblue')
f.tight_layout()



