import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from windrose import WindroseAxes # pip3 install windrose
import cmocean
import os
import datetime

__author__ = "Larissa de Freitas Ramos Jacinto"
__email__ = "larissafreita@gmail.com"
"""
This class has functions that generates subplots of windroses graphs based on daily cycle and the seasons of year.
"""

class Windrose_Functions:
#######################Definining functions###################################
    def __init__(self):
        pass


    def plot_windrose(self, dataframe,direction,speed,ax, levels,plot_legend = True):
        ax.bar(dataframe[direction],dataframe[speed],nsector=16, bins=[0,1,2,3,4],cmap=cmocean.cm.haline,\
            normed=True,opening=0.8,edgecolor='white')
        ax.set_yticks(levels) ;ax.set_yticklabels(levels)
        if plot_legend == True:
            ax.legend(units="m/s",loc = (0.93,0),fontsize=14)

    #Functions based on daily cycle
    def select_period_of_day(self, dataframe, period):
        period_of_day ={'00h_5h45': ['00:00','05:45'],'06h_11h45':['06:00','11:45'],\
            '12h_17h45':['12:00','17:45'],'18h_23h45': ['18:00','23:45'],'all_day':['00:00','23:45']}
        dataframe = dataframe.between_time(period_of_day[period][0],period_of_day[period][1])
        return dataframe

    def plot_windrose_by_period_of_day(self, df,direction, speed,ax, period, levels = np.arange(10, 35, step=5),plot_legend = True):
        dataframe = self.select_period_of_day(df, period)
        self.plot_windrose(dataframe,direction, speed, ax, levels = levels,plot_legend = plot_legend)

    #Functions based on annual cycle (seasons)
    def select_season(self,dataframe, season):
        dict_seasons ={'summer': dataframe[(dataframe.index.month <= 2) | (dataframe.index.month == 12 )],\
            'autumn':dataframe[(dataframe.index.month >= 3) & (dataframe.index.month <= 5 )],\
            'winter':dataframe[(dataframe.index.month >= 6) & (dataframe.index.month <= 8 )],\
            'spring': dataframe[(dataframe.index.month >= 9) & (dataframe.index.month <= 11 )]}
        dataframe = dict_seasons[season]
        return dataframe

    def plot_windrose_by_period_of_year(self,df,direction, speed,ax,season, levels = np.arange(10, 35, step=5),plot_legend = True):
        dataframe = self.select_season(df, season)
        self.plot_windrose(dataframe,direction, speed, ax, levels = levels,plot_legend = plot_legend)

    def save_figure(self,fig_name):
        plt.savefig('{}.png'.format(fig_name),bbox_inches='tight', facecolor='w', edgecolor='w')

    def subplot_seasons(self,dataframe,direction, speed,levels, fig_name):
        list_seasons = [['summer','autumn'],['winter','spring']]
        gs = gridspec.GridSpec(2, 2)
        fig = plt.figure(figsize=(12,10))
        for i in [0,1]:
            for j in [0,1]:
                ax = fig.add_subplot(gs[i,j], projection="windrose")
                self.plot_windrose_by_period_of_year(dataframe,direction, speed, ax, list_seasons[i][j],levels,plot_legend = False)
                ax.set_title(list_seasons[i][j],loc='left',fontsize=14)
                if i ==0 and j ==1:
                    ax.legend(units="m/s",loc = 'lower center',bbox_to_anchor=(-0.25, -0.3),fontsize=11)
        self.save_figure(fig_name)

    def subplot_daily_cycle(self,dataframe,direction, speed,levels, fig_name):
        list_periods = [['00h_5h45','06h_11h45','12h_17h45'],['18h_23h45','all_day']]
        gs = gridspec.GridSpec(2, 3)
        fig = plt.figure(figsize=(15,10))
        for i in [0,1]:
            for j in [0,1,2]:
                if i ==1 and j ==2:
                    ax.legend(units="m/s",loc = 'center',bbox_to_anchor=(1.75, 0.5),fontsize=16)
                else:
                    ax = fig.add_subplot(gs[i,j], projection="windrose")
                    self.plot_windrose_by_period_of_day(dataframe,direction, speed, ax, list_periods[i][j], levels,plot_legend = False)
                    ax.set_title(list_periods[i][j],loc='left',fontsize=14)
                    
        self.save_figure(fig_name)
    ##############################################################################################################


