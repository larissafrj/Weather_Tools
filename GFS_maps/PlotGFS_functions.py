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

__author__ = "Larissa de Freitas Ramos Jacinto"
__email__ = "larissafreita@gmail.com"

"""PlotGFS_functions.py: This class has functions for plot weather maps using GFS model data."""

class PlotGFS_functions:

    def __init__(self):
        self.size = 15
        self.step = 8
        
    def calc_streamlines(self,dset,level_Pa):
        uvel, lonu = add_cyclic_point(np.array(dset.UGRD_P0_L100_GLL0.loc[level_Pa,:,:]), coord=dset.lon_0)
        vvel, lonv = add_cyclic_point(np.array(dset.VGRD_P0_L100_GLL0.loc[level_Pa,:,:]), coord=dset.lon_0)
        lat_stream = dset.lat_0
        lonu = np.where(lonu>=180.,lonu-360.,lonu)
        return lonu, lat_stream, uvel, vvel

    def calculate_absvort(self,dset,level_Pa=50000.):

        dx, dy = mpcalc.lat_lon_grid_deltas(np.array(dset.lon_0),np.array(dset.lat_0))
        f = mpcalc.coriolis_parameter(np.deg2rad(dset.lat_0)).to(units('1/sec'))
        u = np.array(dset.UGRD_P0_L100_GLL0.loc[level_Pa,:,:])*units('m/s')
        v = np.array(dset.VGRD_P0_L100_GLL0.loc[level_Pa,:,:])*units('m/s')
        AbsVort = mpcalc.vorticity(u,v, dx, dy, dim_order='yx')*100000
        return AbsVort

    def calc_thickness(self,dset):
        tmed = (dset.TMP_P0_L100_GLL0.loc[100000.,:,:]+
                dset.TMP_P0_L100_GLL0.loc[50000.,:,:])/2
        thickness = ((287*tmed)/9.8)*np.log(1000/500)  
        return thickness

    def calc_specific_humidity(self, dset,level_Pa):
        es=6.112*np.exp(17.67*(dset.TMP_P0_L100_GLL0.loc[level_Pa,:,:]-273)/
                        ((dset.TMP_P0_L100_GLL0.loc[level_Pa,:,:]-273)+243.5))
        e=dset.RH_P0_L100_GLL0.loc[level_Pa,:,:]*es/100
        Spcf_Hmd=e*622.0/((level_Pa/100)-e) 
        return Spcf_Hmd

    def calc_wnd_spd(self, dset, level_Pa):
        wnd_spd = np.sqrt((np.power(np.array(dset.UGRD_P0_L100_GLL0.loc[level_Pa,:,:]),2)+
                           np.power(np.array(dset.VGRD_P0_L100_GLL0.loc[level_Pa,:,:]),2)))
        return wnd_spd

    def date_info(self, dset):
        initial_time = datetime.datetime.strptime(dset['TMP_P0_L103_GLL0'].attrs['initial_time'], "%m/%d/%Y (%H:%M)")
        forecast_time = dset['TMP_P0_L103_GLL0'].attrs['forecast_time'][0]
        dateTimeObj = initial_time  + relativedelta(hours=int(forecast_time))
        return initial_time, forecast_time, dateTimeObj

    def base_of_the_fig(self,ax, dset,proj):
        ax.set_extent([float(dset.lon_0.min())-360, float(dset.lon_0.max())-360,float(dset.lat_0.min()), 
                       float(dset.lat_0.max())], proj) 
        states = cfeature.NaturalEarthFeature(category='cultural', scale='50m', facecolor='none',
                                              name='admin_1_states_provinces_shp')
        ax.add_feature(cfeature.COASTLINE, linewidth=1, edgecolor='black')
        ax.add_feature(cfeature.BORDERS, linewidth=1, edgecolor='black')
        ax.add_feature(states, linewidth=0.2, edgecolor='k')


    def set_credits(self,ax, dset):
        ax.text(min(dset.lon_0)-360, min(dset.lat_0)-1, 
                'Author: Larissa de Freitas R Jacinto - GitHub: Larissafrj',
                horizontalalignment='left', verticalalignment='top', fontsize=14)

    def set_initial_time(self, ax,dset,initial_time):
        ax.text(max(dset.lon_0)-385, min(dset.lat_0)-1, 'Init Time: {}'.format(initial_time.strftime("%d/%m/%Y %Hz")),
                horizontalalignment='left', verticalalignment='top', fontsize=self.size)

    def save_figure(self,fig_name,dateTimeObj):
        plt.savefig('figures/{}_{}.png'.format(fig_name, dateTimeObj.strftime("%d%m%Y%Hz")),
                bbox_inches='tight', dpi=150, facecolor='w', edgecolor='w')
        plt.close()

    #Wind (Barbs) and temperature (shaded) at surface
    def sfc_wind_temp(self,dset):
        initial_time, forecast_time, dateTimeObj = self.date_info(dset)
        plt.figure(figsize=(15,12))
        proj  =  ccrs.PlateCarree()
        ax = plt.axes(projection=proj)
        self.base_of_the_fig(ax, dset, proj)
        plt.contourf(dset.lon_0, dset.lat_0, dset.TMP_P0_L103_GLL0.loc[2.,:,:]-273.15,transform=proj,
                    cmap=get_cmap('RdYlBu_r'), levels = np.arange(-9,43,0.5),extend='both')
        cbar = plt.colorbar(ax=ax, shrink=0.8,pad = 0,extendrect = True, ticks= np.arange(-9,44,3))
        cbar.ax.tick_params(labelsize=self.size)
        cbar.set_label('2-meter temperature (°C)', fontsize=self.size)

        lines = ax.contour(dset.lon_0, dset.lat_0, dset.TMP_P0_L103_GLL0.loc[2.,:,:]-273.15, 
                         colors = 'grey', levels = np.arange(-6,42,3),linewidths = 0.4,transform=proj)
        clbs = plt.clabel(lines, fontsize=14,fmt='%d')


        plt.barbs(dset.lon_0[::self.step], dset.lat_0[::self.step], 
                  dset.UGRD_P0_L103_GLL0.loc[10.,::self.step,::self.step]*1.94384,
                  dset.VGRD_P0_L103_GLL0.loc[10.,::self.step,::self.step]*1.94384,flip_barb = True,
                  color='k',transform=proj)

        ax.set_title('GFS 0.5 | 2-meter temperature (°C) \nWinds at 10m (kt)', fontsize=self.size, loc='left')
        ax.set_title('{}'.format(dateTimeObj.strftime("%d/%m/%Y %Hz")), fontsize=self.size, loc='right')
        self.set_initial_time(ax,dset,initial_time)
        self.set_credits(ax, dset)
        self.save_figure('sfc_wind_temp',dateTimeObj)

    #Sea Level Pressure (contour) and Thickness (shaded)
    def slp_thickness(self,dset):
        thickness = self.calc_thickness(dset)
        initial_time, forecast_time, dateTimeObj = self.date_info(dset)

        plt.figure(figsize=(15,12))
        proj  =  ccrs.PlateCarree()
        ax = plt.axes(projection=proj)
        self.base_of_the_fig(ax, dset, proj)

        plt.contourf(dset.lon_0, dset.lat_0, thickness,transform=proj,
                     cmap=get_cmap('Spectral_r'), levels = np.arange(5150,5955,5), extend='both')
        cbar = plt.colorbar(ax=ax, shrink=0.8,pad = 0,extendrect = True,ticks= np.arange(5150,6050,50))
        cbar.ax.tick_params(labelsize=self.size)
        cbar.set_label('1000-500 hPa Thickness (m)', fontsize=self.size)

        CS = plt.contour(dset.lon_0, dset.lat_0,dset.PRMSL_P0_L101_GLL0/100, 
                         colors ='navy',levels = np.arange(970,1024,3))
        clbls = ax.clabel(CS, inline=0.7, fontsize=self.size,fmt='%d')

        ax.set_title('GFS 0.5 | MSLP (hPa) \n1000-500 hPa Thickness (m)', fontsize=self.size, loc='left')
        ax.set_title('{}'.format(dateTimeObj.strftime("%d/%m/%Y %Hz")), fontsize=self.size, loc='right')
        self.set_initial_time(ax,dset,initial_time)
        self.set_credits(ax, dset)
        self.save_figure('SLP_Thickness',dateTimeObj)

    #Wind (Streamlines) and Specific Humidity (shaded)
    def streamlines_specific_humidity(self,dset,level_Pa):
        #Reference: https://ncar-hackathons.github.io/visualization/examples/example-Streamlines.html#load-the-dataset


        lonu, lat_stream, uvel, vvel= self.calc_streamlines(dset,level_Pa)
        Spcf_Hmd = self.calc_specific_humidity(dset,level_Pa)
        initial_time, forecast_time, dateTimeObj = self.date_info(dset)

        plt.figure(figsize=(15,12))
        proj  =  ccrs.PlateCarree()
        ax = plt.axes(projection=proj)
        self.base_of_the_fig(ax, dset, proj)

        plt.contourf(dset.lon_0, dset.lat_0, Spcf_Hmd,transform=proj,
                     cmap=get_cmap('Greens'), levels = np.arange(6,15.1,0.1), extend='both')
        cbar = plt.colorbar(ax=ax, shrink=0.8,pad = 0,extendrect = True,ticks= np.arange(6,15.1,1))
        cbar.ax.tick_params(labelsize=self.size)
        cbar.set_label('Specific Humidity (g/kg)', fontsize=self.size)

        ax.streamplot(lonu, lat_stream ,uvel, vvel,linewidth=0.5,
                      arrowsize = 0.6, density=5, color='k',
                       transform=ccrs.PlateCarree() )

        ax.set_title('GFS 0.5 | {} hPa - Specific Humidity (g/kg) \n{} hPa -  Winds'.format(round(level_Pa/100),
                                                                                            round(level_Pa/100)),
                     fontsize=self.size, loc='left')
        ax.set_title('{}'.format(dateTimeObj.strftime("%d/%m/%Y %Hz")), fontsize=self.size, loc='right')
        self.set_initial_time(ax,dset,initial_time)
        self.set_credits(ax, dset)
        self.save_figure('Streamlines_SpecificHumidity_{}hPa'.format(round(level_Pa/100)),dateTimeObj)

    #Wind (Streamlines) and Wind Speed (shaded)
    def streamlines_jet(self,dset,level_Pa):
    #Reference: https://ncar-hackathons.github.io/visualization/examples/example-Streamlines.html#load-the-dataset
        lonu, lat_stream, uvel, vvel= self.calc_streamlines(dset,level_Pa)
        wind_speed = self.calc_wnd_spd(dset, level_Pa)

        initial_time, forecast_time, dateTimeObj = self.date_info(dset)
        
        plt.figure(figsize=(15,12))
        proj  =  ccrs.PlateCarree()
        ax = plt.axes(projection=proj)
        self.base_of_the_fig(ax, dset, proj)
        plt.contourf(dset.lon_0, dset.lat_0, wind_speed,transform=proj,
                    cmap=get_cmap('YlOrRd'), levels = np.arange(10,141,2), extend='max')
        cbar = plt.colorbar(ax=ax, shrink=0.8,pad = 0,extendrect = True,ticks= np.arange(10,141,10))
        cbar.ax.tick_params(labelsize=self.size)
        cbar.set_label('{} hPa - Streamjet (m/s)'.format(round(level_Pa/100)), fontsize=self.size)
        
        ax.streamplot(lonu, lat_stream ,uvel, vvel,linewidth=0.5,
                    arrowsize = 0.6, density=5, color='k',
                    transform=ccrs.PlateCarree() )

        ax.set_title('GFS 0.5 | {} hPa - Winds (m/s)'.format(round(level_Pa/100)), fontsize=self.size, loc='left')
        ax.set_title('{}'.format(dateTimeObj.strftime("%d/%m/%Y %Hz")), fontsize=self.size, loc='right')
        self.set_credits(ax, dset)
        self.set_initial_time(ax,dset,initial_time)
        self.save_figure('Streamlines_jet_{}hPa'.format(round(level_Pa/100)),dateTimeObj)

    #Sea Level Pressure(contour - blue), CAPE (shaded)  and Lifted Index( Contour - Reds)
    def slp_cape_li(self,dset):
        initial_time, forecast_time, dateTimeObj = self.date_info(dset)
        
        plt.figure(figsize=(15,12))
        proj  =  ccrs.PlateCarree()
        ax = plt.axes(projection=proj)
        self.base_of_the_fig(ax, dset, proj)
        plt.contourf(dset.lon_0, dset.lat_0, dset.CAPE_P0_L1_GLL0,transform=proj,cmap=get_cmap('Spectral_r'),
                    levels = np.arange(500,2010,10),extend='max')
        cbar = plt.colorbar(ax=ax, shrink=0.8,pad = 0,extendrect = True,ticks= np.arange(500,2100,100))
        cbar.ax.tick_params(labelsize=self.size)
        cbar.set_label('CAPE (J/Kg)', fontsize=self.size)

        CS = plt.contour(dset.lon_0, dset.lat_0, dset.PRMSL_P0_L101_GLL0/100, colors ='navy',
        levels = np.arange(970,1024,2))
        clbls = ax.clabel(CS, inline=1, fontsize=10,fmt='%d')

        CS = plt.contour(dset.lon_0, dset.lat_0, dset.LFTX_P0_L1_GLL0, 
                        cmap=get_cmap('Reds'), levels = np.arange(-10,0,1))
        clbls = ax.clabel(CS, inline=1, fontsize=10,fmt='%d')

        ax.set_title('GFS 0.5 | MSLP (hPa) \nCAPE (J/Kg) | Lifted Index', fontsize=self.size,loc='left')
        ax.set_title('{}'.format(dateTimeObj.strftime("%d/%m/%Y %Hz")), fontsize=self.size, loc='right')
        self.set_credits(ax, dset)
        self.set_initial_time(ax,dset,initial_time)
        self.save_figure('SLP_cape_LI',dateTimeObj)


    def absvort_geoheight_omega(self,dset,level_Pa):
         #http://glossary.ametsoc.org/wiki/Vorticity
        #https://journals.ametsoc.org/mwr/article/134/10/2649/67332/Mechanisms-for-the-Generation-of-Mesoscale

        AbsVort = self.calculate_absvort(dset,level_Pa)
        initial_time, forecast_time, dateTimeObj = self.date_info(dset)
        
        plt.figure(figsize=(15,12))
        proj  =  ccrs.PlateCarree()
        ax = plt.axes(projection=proj)
        self.base_of_the_fig(ax, dset, proj)
        plt.contourf(dset.lon_0, dset.lat_0, dset.ABSV_P0_L100_GLL0.loc[level_Pa,:,:]*10000,transform=proj,
                    cmap=get_cmap('Blues_r'),levels = np.arange(-6,0.1,0.1),extend='min')
        cbar = plt.colorbar(ax=ax, shrink=0.8,pad = 0,extendrect = True,ticks= np.arange(-6,1,1))
        cbar.ax.tick_params(labelsize=self.size)
        cbar.set_label('Absolute Vorticity ((10⁵)1/s²)', fontsize=self.size)

        CS = plt.contour(dset.lon_0, dset.lat_0, dset.HGT_P0_L100_GLL0.loc[level_Pa,:,:], 
                        colors ='navy',levels= np.arange(4800,6000,100))
        clbls = ax.clabel(CS, inline=1, fontsize=12,fmt='%d')

        CS = plt.contour(dset.lon_0, dset.lat_0, dset.VVEL_P0_L100_GLL0.loc[level_Pa,:,:], 
                        colors ='red',levels= np.arange(-7,0,1))
        clbls = ax.clabel(CS, inline=1, fontsize=12,fmt='%d')
        
        ax.set_title('GFS 0.5 | {} hPa Geopotential Height (gpm) \nAbsolute Vorticity ((10ˆ5)1/s²) | Omega (Pa/s'.format(round(level_Pa/100)), 
                fontsize=self.size, loc='left')
        ax.set_title('{}'.format(dateTimeObj.strftime("%d/%m/%Y %Hz")), fontsize=self.size, loc='right')
        self.set_credits(ax, dset)
        self.set_initial_time(ax,dset,initial_time)
        self.save_figure('AbsVort_GeoHeight_omega_{}hPa'.format(round(level_Pa/100)),dateTimeObj)

    def wind_temp(self,dset, level_Pa):
        initial_time, forecast_time, dateTimeObj = self.date_info(dset)
        
        plt.figure(figsize=(15,12))
        proj = ccrs.PlateCarree()
        ax = plt.axes(projection=proj)
        self.base_of_the_fig(ax, dset, proj)
        plt.contourf(dset.lon_0, dset.lat_0,dset.TMP_P0_L100_GLL0.loc[level_Pa,:,:]-273.15, 
                        cmap=get_cmap('Spectral_r'),levels = np.arange(-9,43,0.1),extend = 'both')
        cbar = plt.colorbar(ax=ax, shrink=0.8,pad = 0,extendrect = True,ticks=  np.arange(-9,44,3))
        cbar.ax.tick_params(labelsize=self.size)
        cbar.set_label('Temperature (°C)', fontsize=self.size)

        plt.barbs(dset.lon_0[::self.step], dset.lat_0[::self.step], dset.UGRD_P0_L100_GLL0.loc[level_Pa,::self.step,::self.step]*1.94384,
                dset.VGRD_P0_L100_GLL0.loc[level_Pa,::self.step,::self.step]*1.94384,
                color='k',transform=proj)
        ax.set_title('GFS 0.5 | {} hPa - Temperature (°C) \n{} hPa - Winds (kt)'.format(round(level_Pa/100),
                                                                                        round(level_Pa/100)),
                    fontsize=self.size, loc='left')
        ax.set_title('{}'.format(dateTimeObj.strftime("%d/%m/%Y %Hz")), fontsize=self.size, loc='right')
        self.set_credits(ax, dset)
        self.set_initial_time(ax,dset,initial_time)
        self.save_figure('Wind_Temp_{}hPa'.format(round(level_Pa/100)),dateTimeObj)

