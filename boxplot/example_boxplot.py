import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

__author__ = "Larissa de Freitas Ramos Jacinto"
__email__ = "larissafreita@gmail.com"

"""example_boxplot.py: 
This routine generates boxplot graphs from using a dataset of weather variables
available in Kaggle.com."""


#dataframe = pd.read_csv('example_boxplot.csv', sep = ';')
""""
Example using a Dataset from Kaggle 
 https://www.kaggle.com/nicholasjhana/energy-consumption-generation-prices-and-weather

"""
dataframe = pd.read_csv('../Dataset_from_Kaggle/weather_features.csv', sep = ',',na_values='NaN')

#Selecting only Seville data.
dataframe = dataframe[dataframe.city_name =='Valencia'].reset_index(drop = True)

dataframe.dt_iso = pd.to_datetime(dataframe.dt_iso,format ='%Y-%m-%d %H:%M:%S%z', utc =True)
dataframe.set_index('dt_iso', inplace=True)

def config_boxplot(x,y,dataframe,axis):
    return sns.boxplot(x = x,y = y, data=dataframe,ax = axis, color="white",\
        medianprops={'color':'green','linewidth':1},boxprops = {'edgecolor':'royalblue','linewidth':1},\
            whiskerprops={'color':'royalblue','linewidth':1},capprops={'color':'royalblue','linewidth':1},\
                flierprops={'markerfacecolor':'white','markeredgecolor':'k','marker':'o', 'markersize':4,'linewidth':0.5})

def save_figure(fig_name):
        plt.savefig('{}.png'.format(fig_name),bbox_inches='tight', facecolor='w', edgecolor='w')

def config_fig_boxplot(x, y, dataframe, xticks, labels,fig_name):
    fig,ax = plt.subplots(figsize=(14, 10))
    config_boxplot(x,y,dataframe,ax)
    plt.xlabel(labels[0]); ax.set_ylabel(labels[1])
    ax.set_xticklabels(xticks)
    save_figure(fig_name)

xticks = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
labels = ['Hour', 'Wind Speed']
config_fig_boxplot(dataframe.index.hour,dataframe.wind_speed, dataframe, xticks, labels,'Valencia_hourly_wnd_spd') 

xticks = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
labels = ['Month', 'Wind Speed']
config_fig_boxplot(dataframe.index.month,dataframe.wind_speed, dataframe, xticks, labels,'Valencia_monthly_wnd_spd') 

xticks = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
labels = ['Hour', 'Temperature']
config_fig_boxplot(dataframe.index.hour,dataframe.temp-273, dataframe, xticks, labels,'Valencia_hourly_temp') 

xticks = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
labels = ['Month', 'Temperature']
config_fig_boxplot(dataframe.index.month,dataframe.temp-273, dataframe, xticks, labels,'Valencia_monthly_temp') 
