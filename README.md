<h1>Weather_Tools Project </h1>

This project has some codes that I created in the last years to simplify my routine as a meteorologist at work. Here you will also find codes that I developed to view the weather data for my M.Sc. thesis.


<h1>Motivation </h1>

This repository aims to help other students who are starting to use python, giving examples about how this language can be used for download and visualize different types of meteorological data.

<h1>Instalation </h1>

All codes where developed using Python 3.x.
I promise that I will upload the requirement.txt later.

<h1>Description </h1>

<h3>models/</h3>

Codes for download meteorological models outputs.

  download_gfs.py - This code downloads the GFS predictions from one of the lastest 15 days available on the NCEP website with 6 hours of a time step. The user can select the initial day and hour, the GFS resolution (0p25, 0p50, or 1p00), and how many days of prediction will be downloaded (eg. type 0.5 for 12h, 1 for 1 day, etc).
  
  download_gfs_graph.py - This version of download_gfs.py has a Graphical User Interface to turn more friendly the selection of the GFS configuration's preferences.
  
  download_wrf_model.py - This code downloads the WRF predictions available in CPTEC/INPE website with 6 hours of the time step. The user can select the initial day and hour and how many days of prediction will be downloaded (eg. type 0.5 for 12h, 1 for 1 day, etc). This WRF model has 5km of horizontal resolution and a domain that includes South America.
  
<h3>skew_t_wyoming/</h3>

Codes to catch atmospheric soundings data and plot the skew-T graph.

   skewT_functions.py - This class has functions to extract and organize the atmospheric sounding data from the University of Wyoming website using web scraping techniques (BeautifulSoup package) and plots the Skew-T graph using Metpy package.
   
  example_skew_t.py - This code has an example for the SBCT airport (id 83840).

<h3>boxplot/</h3>

<h3>windrose/</h3>
