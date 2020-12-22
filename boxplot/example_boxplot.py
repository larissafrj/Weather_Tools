import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

__author__ = "Larissa de Freitas Ramos Jacinto"
__email__ = "larissafreita@gmail.com"

"""example_boxplot.py: 
This routine generates boxplot graphs from using a dataframe with random values of wind speed."""


dataframe = pd.read_csv('example_boxplot.csv', sep = ';')

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
config_fig_boxplot('Hour','Int', dataframe, xticks, labels,'example_hourly') 

xticks = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
labels = ['Month', 'Wind Speed']
config_fig_boxplot('Month','Int', dataframe, xticks, labels,'example_monthly') 
