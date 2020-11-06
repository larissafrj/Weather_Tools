import pandas as pd
import datetime
from skewT_functions import skewT_functions
skewT_functions = skewT_functions()

date = datetime.datetime(2020,8,6,0)
location_id = 83840
df_sounding, df_instability_index = skewT_functions.extract_soundings(date, location_id)
skewT_functions.plot_soundings(date, location_id, df_sounding, df_instability_index)
skewT_functions.download_soundings(date, location_id)