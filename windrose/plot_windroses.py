#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 20:20:47 2018
This routine generate windroses graphs.
Script para gerar rosas dos ventos a partir dos dados tratados da torre A - 10m
período: 1982 - 2001


@author: Larissa de Freitas Ramos Jacinto
"""



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#usar o comando sudo pip3 install windrose
from windrose import WindroseAxes
import cmocean
import os
import datetime

# In[especificação da pasta onde ficará cada figura]
PATH = '/Volumes/LARISSA'
loc_dado =PATH+'/Mestrado/resultados_dissertacao/dados_torres/dados_1982_2001/dados_tratados/'
loc_fig = PATH+'/Mestrado/resultados_dissertacao/resultados_windrose/1982_2001/torre_a10/'


# In[abrindo os dataset .csv com separador (,) de cada Torre]


# Torre A - 10m
mydateparser = lambda x: datetime.datetime.strptime(x, '%Y %m %d %H')
dataframe = pd.read_csv(loc_dado+'TORREA10.csv', sep = ',',na_values='NaN',parse_dates={'Date': ['Ano','Mes','Dia','Hora']},date_parser= mydateparser, index_col = 'Date')
#torre_a10 = torre_a10.loc[:,'Vel','Dir']

def axes():

    fig=plt.figure(figsize=(8, 8), dpi=80, facecolor='w', edgecolor='w')
    rect=[0.05,0.05,0.8,0.85] 
    wa=WindroseAxes(fig, rect)
    fig.add_axes(wa)
    return wa

def plot_windrose(dataframe, levels = np.arange(10, 70, step=10),\
    plot_legend = True, save_figure = True,fig_name = 'Example_windrose'):

    wa = axes()
    wa.bar(dataframe['Dir'], dataframe['Vel'],nsector=16, bins=[1,2,3,4],cmap=cmocean.cm.haline,\
        normed=True,opening=0.8,edgecolor='white')
    wa.set_yticks(levels) ;wa.set_yticklabels(levels)
    if plot_legend == True:
        wa.legend(units="m/s",loc = (0.93,0),fontsize=11) 
    if save_figure == True:
        plt.savefig('{}.png'.format(fig_name))
    elif save_figure == False:
        plt.show()

def select_period_of_day(dataframe, period):
    period_of_day ={'00h_5h45': ['00:00','05:45'],'06h_11h45':['06:00','11:45'],\
        '12h_17h45':['12:00','17:45'],'18h_23h45': ['18:00','23:45']}
    dataframe = dataframe.between_time(period_of_day[period][0],period_of_day[period][1])  
    return dataframe

def plot_windrose_by_period_of_day(df,period, levels = np.arange(10, 70, step=10),plot_legend = True):
    dataframe = select_period_of_day(df, period)
    plot_windrose(dataframe, levels = np.arange(10, 70, step=10),plot_legend = True)


#montar funcao pra estacoes do ano
def plot_windrose_by_period_of_year(dataframe,season,plot_legend = True):
    dict_seasons ={'summer': dataframe[(dataframe.index.month <= 2) | (dataframe.index.month == 12 )],\
        'autumn':dataframe[(dataframe.index.month >= 3) & (dataframe.index.month <= 5 )],\
        'winter':dataframe[(dataframe.index.month >= 6) & (dataframe.index.month <= 8 )],\
        'spring': dataframe[(dataframe.index.month >= 9) & (dataframe.index.month <= 11 )]}

    dataframe = dict_seasons[season]
    wa = axes()
    wa.bar(dataframe['Dir'], dataframe['Vel'],nsector=16, bins=[1,2,3,4],cmap=cmocean.cm.haline,\
        normed=True,opening=0.8,edgecolor='white')
   # wa.set_yticks(np.arange(10, 70, step=10))
    if plot_legend == True:
        wa.legend(units="m/s",loc = (0.93,0),fontsize=11)
    plt.show()

#print(dataframe[(dataframe.index.month <= 2) | (dataframe.index.month == 12 )])
#print(dataframe[(dataframe.index.month >= 3) & (dataframe.index.month <= 5 )])
#plot_windrose(dataframe)
plot_windrose_by_period_of_day(dataframe,'00h_5h45',plot_legend=True)
#wa.legend(units="m/s",loc = (0.95,0),fontsize=11)
plt.show()
import sys
sys.exit()
#plt.savefig(loc_fig+"torre_a10.png", dpi=None, facecolor='w', edgecolor='w',orientation='portrait')
#plt.close('all')
#    period_of_day ={'00h_5h45': ['00:00','05:45'],'06h_11h45':['06:00','11:45'],\
#        '12h_17h45':['12:00','17:45'],'18h_23h45': ['18:00','23:45']}
#    dataframe = dataframe.between_time(period_of_day[0],period_of_day[1])
#    return dataframe

#import sys
#sys.exit()
#wa = new_axes()    
