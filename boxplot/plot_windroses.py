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

mydateparser = lambda x: datetime.datetime.strptime(x, '%Y %m %d %H')
dataframe = pd.read_csv('example_windrose.csv', sep = ';',na_values='NaN',parse_dates={'Date': ['Year','Month','Day','Hour']},\
    date_parser= mydateparser, index_col = 'Date')

#dataframe =  pd.read_csv('TORREA10.csv', sep = ',',na_values='NaN',parse_dates={'Date': ['Ano','Mes','Dia','Hora']},\
#    date_parser= mydateparser, index_col = 'Date')
windrose_functions.subplot_seasons(dataframe, np.arange(1, 10, step=2),'example_seasons')
windrose_functions.subplot_daily_cycle(dataframe, np.arange(1, 10, step=2),'example_daily')
