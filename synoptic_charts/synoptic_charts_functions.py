import requests
from datetime import datetime, timedelta
import numpy as np
import os

__author__ = "Larissa de Freitas Ramos Jacinto"
__email__ = "larissafreita@gmail.com"

"""Synoptic_Charts_functions.py: This class has functions to download synoptic charts from 
Marinha and CPTEC websites. 
You can find and example of the use of this class in the example_synoptic_charts.py code.
"""

class Synoptic_Charts_functions:
    #initial_date and last_date must be strings in day/month/Year format.
    #institution_responsible must be 'Marinha do Brasil' or 'CPTEC'
    def __init__(self,initial_date,last_date,institution_responsible):
        self.dirnames = {'MARINHA DO BRASIL': 'marinha_charts', 'CPTEC': 'cptec_charts'}
        self.initial_date = initial_date
        self.last_date = last_date
        self.institution_responsible = institution_responsible
        self.start = datetime.strptime(self.initial_date, "%d/%m/%Y")
        self.end = datetime.strptime(self.last_date, "%d/%m/%Y")

    #It creates and directory for each institution.
    def create_dirs(self):
        try:
            os.makedirs(self.dirnames[self.institution_responsible.upper()])
        except OSError:
            if os.path.exists(self.dirnames[self.institution_responsible.upper()]):
                pass
            else:
                raise
    #It downloads the synoptic charts and saves them.   
    def download_synoptic_charts(self):
        
        if self.institution_responsible.upper() == 'MARINHA DO BRASIL':
            interval = (self.end - self.start).days
            times = range(0, 24*interval, 12)
            date_vector = np.array([self.start + timedelta(hours=i) for i in times])
        if self.institution_responsible.upper() == 'CPTEC':
            interval = (self.end - self.start).days
            times = range(0, 24 * interval, 6)
            date_vector = np.array([self.start + timedelta(hours=i) for i in times])

        self.create_dirs()
        for i in date_vector:

            if self.institution_responsible.upper() == 'MARINHA DO BRASIL':
                url ='https://www.marinha.mil.br/chm/sites/www.marinha.mil.br.chm/files/cartas-sinoticas/c{}{}{}{}.jpg'.format(
                    i.strftime('%y'), i.strftime('%m'), i.strftime('%d'), i.strftime('%H'))

            if self.institution_responsible.upper() == 'CPTEC':
                url = 'http://img0.cptec.inpe.br/~rgptimg/Produtos-Pagina/Carta-Sinotica/Analise/Superficie/superficie_{}{}{}{}.gif'.format(
                    i.strftime('%Y'), i.strftime('%m'), i.strftime('%d'), i.strftime('%H'))

            r = requests.get(url)
            with open('{}/{}/chart_{}{}{}_{}z.jpg'.format(os.getcwd(),self.dirnames[self.institution_responsible.upper()],
                    i.strftime('%d'), i.strftime('%m'), i.strftime('%Y'), i.strftime('%H')), 'wb') as f:
                f.write(r.content)
                f.close()

