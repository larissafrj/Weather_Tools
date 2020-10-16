from datetime import datetime, timedelta, date
from download_models import download_models


"""download_wrf_model.py: This routine dowload the output files from predictions of 
the Global Forecast System Model based on the user's preferences.

link: http://ftp.cptec.inpe.br/modelos/tempo/WRF/ams_05km/recortes/pos/"""
__author__ = "Larissa de Freitas Ramos Jacinto"
__email__ = "larissafreita@gmail.com"

initial_date = input('Insert the initial date of the simulation (Type in format dd/mm/YYYY): ')
initial_hour = input('Insert the initial hour of the simulation (Type: 00z, 06z, 12z or 18z): ')
days_pred = input('How many days of prediction do you want? (Type a number): ')

initial_date = initial_date.split('/')
initial_hour = initial_hour.split('z')

start_date = datetime(int(initial_date[2]), int(initial_date[1]), int(initial_date[0]))
start_hour = int(initial_hour[0])

download_models(days = days_pred).download('WRF', start_date, start_hour)