import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cmocean
import os
import datetime
os.chdir(os.getcwd()+'/windrose/')
from windrose_functions import Windrose_Functions
windrose_functions = Windrose_Functions()

""""
Example using a Dataset from Kaggle 
 https://www.kaggle.com/nicholasjhana/energy-consumption-generation-prices-and-weather

"""
dataframe = pd.read_csv('../Dataset_from_Kaggle/weather_features.csv', sep = ',',na_values='NaN')

#Selecting only Seville data.
dataframe = dataframe[dataframe.city_name =='Seville'].reset_index(drop = True)


dataframe.dt_iso = pd.to_datetime(dataframe.dt_iso,format ='%Y-%m-%d %H:%M:%S%z', utc =True)
dataframe.set_index('dt_iso', inplace=True)

windrose_functions.subplot_seasons(dataframe,'wind_deg','wind_speed', np.arange(5, 30, step=5),'Seville_seasons')
windrose_functions.subplot_daily_cycle(dataframe,'wind_deg','wind_speed', np.arange(5, 30, step=5),'Seville_daily')