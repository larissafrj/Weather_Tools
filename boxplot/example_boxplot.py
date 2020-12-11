#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 12:07:11 2018


script para gerar gráficos de boxplot com os dados de intensidade do ventoda CNAAA com dados de 1982 a 2001
@author: Larissa de Freitas Ramos Jacinto
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dado = pd.read_csv('TORREA10.csv', sep = ',', na_values='nan')

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
labels = ['Horas', 'Intensidade do Vento']
config_fig_boxplot('Hora','Int', dado, xticks, labels,'example_hourly') 

xticks = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']
labels = ['Meses', 'Intensidade do Vento']
config_fig_boxplot('Mes','Int', dado, xticks, labels,'example_monthly') 
# framebox= pd.DataFrame(np.nan, index = np.arange(14880), columns = np.arange(12))
# mensal = pd.DataFrame(np.nan, index = np.arange(14880), columns = np.arange(7))
# framebox.loc[:,:] = np.nan
# for j in range(0,12):
#     mensal = dado.query('Mes == '+str(j+1)+'')
#     mensal = mensal.reset_index()


#     framebox.loc[:,j]= mensal.loc[:,'Vel']
# framebox.columns = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']

# fig =plt.figure(figsize=(20,14), dpi=300, facecolor='w', edgecolor='w')
# letras = ['a)', 'b)', 'c)','d)', 'e)','f)']
# for i in range(0,6):
#     dado = pd.read_csv(loc_dado+'TORRE'+vetor_torres[i]+'.csv', sep = ',', na_values='nan')
#     framebox = pd.DataFrame(np.zeros((14880,12)))
#     mensal = pd.DataFrame(np.zeros((14880,7))) #,index =['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']
#     framebox.loc[:,:] = np.nan
#     for j in range(0,12):
#         mensal = dado.query('Mes == '+str(j+1)+'')
#         mensal = mensal.reset_index()


#         framebox.loc[:,j]= mensal.loc[:,'Vel']
#     framebox.columns = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']

#     ax = fig.add_subplot(2,3,i+1)   
#     ax.set_title(letras[i],loc='left',fontsize=13)

#     framebox.boxplot(grid=False, column =  ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'])       
#     if i==0 or i ==3:
#         plt.ylabel('Wind Speed (m/s)',fontsize=13)
#     if i ==3 or i ==4 or i ==5:
#         plt.xlabel('Month',fontsize=13)

#     if i ==2 or i ==3 or i ==4 or i ==5:
#         plt.ylim([0,4])
#     if i ==0 or i ==1:
#         plt.ylim([0,3.7])
# plt.savefig(loc_fig+'en_subplot_boxplot_mensal_2.png', dpi=300, bbox_inches='tight', facecolor='w', edgecolor='w',orientation='landscape')
# plt.close('all')

# fig =plt.figure(figsize=(20,14), dpi=300, facecolor='w', edgecolor='w')
# letras = ['a)', 'b)', 'c)','d)', 'e)','f)']
# for i in range(0,6):
#     dado = pd.read_csv(loc_dado+'TORRE'+vetor_torres[i]+'.csv', sep = ',', na_values='nan')
#     #framebox = pd.DataFrame(np.zeros((14880,24)))
#     #horario= pd.DataFrame(np.zeros((14880,7))) #,index =['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']
#     framebox= pd.DataFrame(np.nan, index = np.arange(14880), columns = np.arange(24))
#     mensal = pd.DataFrame(np.nan, index = np.arange(14880), columns = np.arange(7))

#     framebox.loc[:,:] = np.nan
#     for j in range(0,24):
#         horario = dado.query('Hora == '+str(j)+'')
#         horario = horario.reset_index()


#         framebox.loc[:,j]= horario.loc[:,'Vel']
#     framebox.columns = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']

#     ax = fig.add_subplot(2,3,i+1)   
#     ax.set_title(letras[i],loc='left',fontsize=13)
#     print(framebox.iloc[:,12:19].describe())
#     framebox.boxplot(grid=False, column =   ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'])       
#     if i==0 or i ==3:
#         plt.ylabel('Wind Speed (m/s)',fontsize=13)
#     if i ==3 or i ==4 or i ==5:
#         plt.xlabel('Hours',fontsize=13)
#     if i ==2 or i ==3 or i ==4 or i ==5:
#         plt.ylim([0,30])
#     if i ==0 or i ==1:
#         plt.ylim([0,3.7])

# plt.tight_layout(pad = 0.5)
# plt.savefig(loc_fig+'subplot_boxplot_horario.png', dpi=300, bbox_inches='tight', facecolor='w', edgecolor='w',orientation='landscape')
# plt.close('all')

#        x = pd.DataFrame([framebox.loc[0,:]])
#        #Figura: temperatura do ar - 10m
#        fig =plt.figure(figsize=(8, 12), dpi=300, facecolor='w', edgecolor='w')
#        ax = fig.add_axes([0.1,0.1,0.88,0.88])
#        plt.boxplot(x[~np.isnan(framebox.loc[0,:])])
#        plt.tight_layout(pad=0.5)
#        plt.savefig(loc_fig+'boxplot_'+vetor_torres[i]+'.png', dpi=200, facecolor='w', edgecolor='w',orientation='landscape')
