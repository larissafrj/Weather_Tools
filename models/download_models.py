
from datetime import datetime,timedelta
import os
import numpy as np
import subprocess
"""download_models.py: This class has a function for automatically download the output files 
of a weather forecast model simulation (GFS model or CPTEC's WRF model)."""


__author__ = "Larissa de Freitas Ramos Jacinto"
__email__ = "larissafreita@gmail.com"

class download_models():
    def __init__(self, days = 1):
        self.days = days
        self.dirnames = {'GFS': 'gfs_files', 'WRF': 'wrf_files'}
        self.end_times = float(days)*24+1
        self.times = range(0, int(self.end_times), 6)

    def create_dirs(self, model):

        try:
            os.makedirs(self.dirnames[model])
        except OSError:
            if os.path.exists(self.dirnames[model]):
                pass
            else:
                raise

    def download(self, model, start_date, start_hour,gfs_resolution ='0p50'):
        self.create_dirs(model)
        self.data_i = datetime(start_date.year, start_date.month, start_date.day)
        self.data_vector = np.array([self.data_i + timedelta(hours=i) for i in self.times])
        if model== 'GFS':
            os.popen('rm {}/{}/*'.format(os.getcwd(),self.dirnames[model]))
            location = '{}/{}'.format(os.getcwd(),self.dirnames[model])

            for i in self.times:
                url = 'ftp://ftp.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{}{}{}/{}/gfs.t{}z.pgrb2.{}.f{}'.format(
                    start_date.strftime('%Y'), start_date.strftime('%m'),start_date.strftime('%d'),str(start_hour).zfill(2),
                    str(start_hour).zfill(2),gfs_resolution, str(i).zfill(3))
                p = subprocess.Popen(['wget','-P', location,url], stdout=subprocess.PIPE)
                (output, err) = p.communicate()  
                p_status = p.wait()


        if model == 'WRF':
            os.popen('rm {}/{}/*'.format(os.getcwd(),self.dirnames[model]))
            location = '{}/{}'.format(os.getcwd(),self.dirnames[model])

            for i in self.data_vector:
                url = 'http://ftp.cptec.inpe.br/modelos/tempo/WRF/ams_05km/recortes/pos/{}/{}/{}/{}/WRF_cpt_05KM_{}{}{}{}_{}{}{}{}.grib2'.format(
                    start_date.strftime('%Y'), start_date.strftime('%m'),start_date.strftime('%d'),start_date.strftime('%H'),
                    start_date.strftime('%Y'), start_date.strftime('%m'),start_date.strftime('%d'),start_date.strftime('%H'),
                    i.strftime('%Y'), i.strftime('%m'), i.strftime('%d'),i.strftime('%H'))
                p = subprocess.Popen(['wget','-P', location,url], stdout=subprocess.PIPE)
                (output, err) = p.communicate()  
                p_status = p.wait()