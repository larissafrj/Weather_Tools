import Nio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import datetime
from dateutil.relativedelta import relativedelta
import xarray as xr
from cartopy.util import add_cyclic_point
import metpy.calc as mpcalc
from metpy.units import units
from PlotGFS_functions import PlotGFS_functions

"""PlotGFS_example.py: This code has an example of application 
to the functions implemented in PlotGFS_functions.py."""

#File from https://www.ncei.noaa.gov/thredds/catalog/model-gfs-g4-anl-files/catalog.html
dset = xr.open_dataset('gfs_4_20200701_0000_000.grb2',engine='pynio')
dset = dset.sel(lat_0=slice(15,-60), lon_0=slice(360-108, 350))

PlotGFS_functions().sfc_wind_temp(dset)
PlotGFS_functions().sfc_wind_temp(dset)
PlotGFS_functions().slp_thickness(dset)
PlotGFS_functions().streamlines_specific_humidity(dset,85000)
PlotGFS_functions().streamlines_jet(dset,20000.)
PlotGFS_functions().streamlines_jet(dset,85000.)
PlotGFS_functions().slp_cape_li(dset)
PlotGFS_functions().absvort_geoheight_omega(dset,50000)
PlotGFS_functions().wind_temp(dset,70000)
PlotGFS_functions().wind_temp(dset,85000)