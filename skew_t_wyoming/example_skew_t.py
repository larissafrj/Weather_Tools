import pandas as pd
import datetime
from skewT_functions import skewT_functions
skewT_functions = skewT_functions()

__author__ = "Larissa de Freitas Ramos Jacinto"
__email__ = "larissafreita@gmail.com"

"""example_skew_t.py: This code has an example of application to the functions implemented in skewT_functions.py."""

date = datetime.datetime(2020,8,6,0)
location_id = 83840
df_sounding, df_instability_index = skewT_functions.extract_soundings(date, location_id)
skewT_functions.plot_soundings(date, location_id, df_sounding, df_instability_index)
skewT_functions.download_soundings(date, location_id)
