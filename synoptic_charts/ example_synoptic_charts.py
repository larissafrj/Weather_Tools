from synoptic_charts_functions import Synoptic_Charts_functions

"""example_synoptic_charts.py: An example of the aplication to the Synoptic_Charts_functions.py.
"""
__author__ = "Larissa de Freitas Ramos Jacinto"
__email__ = "larissafreita@gmail.com"

#Downloading charts from Marinha do Brasil posted between December 15, 2020 and December 18, 2020.
download_charts = Synoptic_Charts_functions('15/12/2020', '18/12/2020','Marinha do Brasil')
download_charts.download_synoptic_charts()
