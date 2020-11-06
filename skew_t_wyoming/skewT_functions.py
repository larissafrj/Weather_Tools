import requests
import numpy as np
import pandas as pd
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units
import wrf
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta
from matplotlib.patches import Rectangle
from matplotlib.cbook import get_sample_data
import os

__author__ = "Larissa de Freitas Ramos Jacinto"
__email__ = "larissafreita@gmail.com"
"""skewT_functions.py: This class has functions to extract data of atmospheric soundings from the University of Wyoming website
(http://weather.uwyo.edu/upperair/sounding.html), and plot the skew-T./"""
class skewT_functions:

    def __init__(self):

        pass

    def create_dirs(self, station):
        try:
            os.makedirs('soundings_{}'.format(station))
        except OSError:
            if os.path.exists('soundings_{}'.format(station)):
                pass
            else:
                raise

    def extract_soundings(self,date, station):
        url = 'http://weather.uwyo.edu/cgi-bin/sounding?region=samer&TYPE=TEXT%3ALIST&YEAR={}&MONTH={}&FROM={}{}&TO={}{}&STNM={}'.format(date.strftime('%Y'),date.strftime('%m'),date.strftime('%d'),
                                                        date.strftime('%H'),date.strftime('%d'),date.strftime('%H'),
                                                        station)

        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')

        #extraindo dataframe com a sondagem
        sounding = soup.select("pre")[0]
        sounding = sounding.get_text()
        sounding = sounding.split('\n')

        pres = hght =temp =dwpt = relh = mixr = drct =sknt =thta = thte = thtv = []
        for i in sounding:
            pres = np.append(pres,i[0:7])   ; hght = np.append(hght,i[7:14])  ; temp = np.append(temp,i[14:21])
            dwpt = np.append(dwpt,i[21:28]) ; relh = np.append(relh,i[28:35]) ; mixr = np.append(mixr,i[35:42])
            drct = np.append(drct,i[42:49]) ; sknt = np.append(sknt,i[49:56]) ; thta = np.append(thta,i[56:63])
            thte = np.append(thte,i[63:70]) ; thtv = np.append(thtv,i[70:77])

        df_sounding = pd.DataFrame([pd.Series(pres).replace('       ', np.nan), pd.Series(hght).replace('       ', np.nan),
                                    pd.Series(temp).replace('       ', np.nan), pd.Series(dwpt).replace('       ', np.nan), 
                                    pd.Series(relh).replace('       ', np.nan), pd.Series(mixr).replace('       ', np.nan),
                                    pd.Series(drct).replace('       ', np.nan), pd.Series(sknt).replace('       ', np.nan), 
                                    pd.Series(thta).replace('       ', np.nan), pd.Series(thte).replace('       ', np.nan), 
                                    pd.Series(thtv).replace('       ', np.nan)]).T
        df_sounding.columns = ['PRES', 'HGHT', 'TEMP', 'DWPT', 'RELH', 'MIXR', 'DRCT', 'SKNT', 'THTA', 'THTE', 'THTV']
        df_sounding.drop(index=[0,1,2,3,4,len(df_sounding)-1], inplace = True)
        df_sounding.reset_index(drop = True, inplace = True)

        #dataframe com os indices de instabilidade da sondagem
        instability_index = soup.select("pre")[1].get_text()
        instability_index = instability_index.split('\n')
        parametros = valores = []

        instability_index = soup.select("pre")[1].get_text() ; instability_index = instability_index.replace('  ', '')
        instability_index = instability_index.replace('\n ', '\n') ; instability_index = instability_index.split('\n')
        instability_index = instability_index[1:-1]

        for k in instability_index:
            i, j = k.split(':')
            parametros = np.append(parametros, i)
            valores = np.append(valores, j.replace(' ', ''))

        df_instability_index = pd.DataFrame([parametros, valores])
        df_instability_index.columns = df_instability_index.loc[0,:]
        df_instability_index.drop(index=[0], inplace = True)
        df_instability_index.reset_index(drop = True, inplace = True)
        return df_sounding, df_instability_index


    def download_soundings(self, date, station):
        self.create_dirs(station)
        df_sounding, df_instability_index = self.extract_soundings(date, station)
        location = '{}/soundings_{}'.format(os.getcwd(),station)
        df_sounding.to_csv('{}/sounding_{}{}{}{}.csv'.format(location, date.strftime('%d'), date.strftime('%m'),date.strftime('%Y'),date.strftime('%H')), sep=',', index=False)
        df_instability_index.to_csv('{}/instability_index_{}{}{}{}.csv'.format(location, date.strftime('%d'), date.strftime('%m'),date.strftime('%Y'),date.strftime('%H')), sep=',', index=False)
        
    def plot_soundings(self, date, station, dataframe, indices):
        self.create_dirs(station)
        location = '{}/soundings_{}'.format(os.getcwd(),station)
        dateTimeObj = date  + relativedelta(hours=-3) #trazendo para o horario local
        p = pd.to_numeric(dataframe['PRES']).values * units.hPa
        T = pd.to_numeric(dataframe['TEMP']).values * units.degC
        Td = pd.to_numeric(dataframe['DWPT']).values * units.degC
        wind_speed = pd.to_numeric(dataframe['SKNT']).values * units.knots
        wind_dir = pd.to_numeric(dataframe['DRCT']).values * units.degrees
        u, v = mpcalc.wind_components(wind_speed, wind_dir)   

        df_notnull = dataframe.dropna()
        p_notnull = pd.to_numeric(df_notnull['PRES']).values * units.hPa
        T_notnull = pd.to_numeric(df_notnull['TEMP']).values * units.degC
        Td_notnull = pd.to_numeric(df_notnull['DWPT']).values * units.degC
        i = 0
        fig = plt.figure(figsize=(12, 9))
        skew = SkewT(fig, rotation=45)
        skew.plot(p, T, 'r')
        skew.plot(p, Td, 'g')
        skew.plot_barbs(p, u, v,flip_barb = True)
        skew.ax.set_ylim(1000, 100)
        skew.ax.set_xlim(-40, 60)
        
        # Calculate LCL height and plot as black dot
        lcl_pressure, lcl_temperature = mpcalc.lcl(p_notnull[i], T_notnull[i], Td_notnull[i])

        #skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')
        
        # Calculate full parcel profile and add to plot as black line
        prof = mpcalc.parcel_profile(p_notnull[i:], T_notnull[i], Td_notnull[i]).to('degC')
        cape, cine = mpcalc.cape_cin(p_notnull, T_notnull, Td_notnull, prof, which_lfc='bottom', which_el='top')

        skew.plot(p_notnull[i:], prof, 'k', linewidth=2)
        # Shade areas of CAPE and CIN
        skew.shade_cin(p_notnull[i:], T_notnull[i:], prof)
        skew.shade_cape(p_notnull[i:], T_notnull[i:], prof)
        # An example of a slanted line at constant T -- in this case the 0 isotherm
        skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)
        # Add the relevant special lines
        skew.plot_dry_adiabats()
        skew.plot_moist_adiabats()
        skew.plot_mixing_lines()
        plt.title('Sondagem Atmosférica  - {} \n{}'.format(indices.loc[0,'Station identifier'],
                                                        dateTimeObj.strftime('%d/%m/%Y às %Hh')), fontsize = 16) #(tempo 7)
        plt.xlabel('Temperatura (°C)', fontsize = 14)
        plt.ylabel('Pressão atmosférica (hPa)', fontsize = 14)
        texto_indices = """CAPE: {} J/kg \n
        CINE: {} J/kg
        \nK: {} \n\nLI: {}
        \nTT: {} 
        \nShowalter: {} 
        \nRi-Bulk: {} 
        \n  Espessura: {} m
        (1000 hPa a 500 hPa)
        \n SWEAT: {}
        \n Temperatura no NCL: {} K
        \n Pressão no NCL: {} hPa""".format(float(str(cape).split(' ')[0]), float(str(cine).split(' ')[0]),
                                            indices.loc[0,'K index'],
                        indices.loc[0,'Lifted index'],indices.loc[0,'Totals totals index'],
                                    indices.loc[0,'Showalter index'], 
                                    indices.loc[0,'Bulk Richardson Number'],
                        indices.loc[0,'1000 hPa to 500 hPa thickness'],indices.loc[0,'SWEAT index'],
                                round((float(str(lcl_temperature).split(' ')[0])+273.25),2),
                                            round(float(str(lcl_pressure).split(' ')[0]),2))
        plt.text(35, 250, texto_indices, 
                ha = "center",va="center",
                bbox=dict(boxstyle="round",ec='goldenrod',fc='lightyellow'),fontsize = 13)
        plt.text(60, 900, 'Author: Larissa de Freitas R Jacinto \n GitHub: Larissafrj'
                    ,horizontalalignment='left', verticalalignment='top', fontsize=14)
                    
        plt.savefig('{}/{}_{}.png'.format(location,indices.loc[0,'Station identifier'],date.strftime('%d%m%Y_%Hz')), 
                    dpi=300,bbox_inches='tight', facecolor='w', edgecolor='w',orientation='landscape')


