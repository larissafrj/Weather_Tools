from datetime import datetime, timedelta, date
import tkinter as tk
from download_models import download_models


__author__ = "Larissa de Freitas Ramos Jacinto"
__email__ = "larissafreita@gmail.com"

"""download_gfs.py: This routine dowload the output files from predictions of 
the Global Forecast System Model based on the user's preferences.
In this version the user can set his preferences using a Graphical User Interface.
link: ftp://ftp.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/"""

   
root=tk.Tk() 
  
# setting the windows size 
root.geometry("600x300") 
   
# Declaration of Tkinter variables (strings)
initial_date=tk.StringVar(); initial_hour=tk.StringVar() 
gfs_resolution=tk.StringVar(); days_prediction=tk.StringVar()
  
   
# Defining a function that will download GFS data
def submit(): 
    gfs_res=gfs_resolution.get() 
    days_pred=days_prediction.get() 
    date = initial_date.get().split('/')
    hour = initial_hour.get().split('z')
    start_date = datetime(int(date[2]), int(date[1]), int(date[0]))
    start_hour = int(hour[0])

    download_models(days = days_pred).download('GFS', start_date, start_hour,gfs_resolution =gfs_res)

    print_label = tk.Label(root, text = 'The outputs are available in gfs_files folder!', 
                       font = ('calibre',10,'bold')); print_label.grid(row=6,column=0) 

def setting_label_entry(root, text, var):
    label = tk.Label(root, text = text, 
                      font=('calibre', 10, 'bold'))  
    entry = tk.Entry(root, textvariable = var,
                      font=('calibre',10,'normal')) 
    return label, entry

# creating a label and an entry for input the initial date 
text_datelabel = 'Insert the initial date of the simulation (Type in format dd/mm/YYYY): '
date_label, date_entry =  setting_label_entry(root, text_datelabel, initial_date)

# creating a label and an entry for input the initial hour
text_hourlabel = 'Insert the initial hour of the simulation (Type: 00z, 06z, 12z or 18z): '
hour_label, hour_entry =  setting_label_entry(root, text_hourlabel, initial_hour)

# creating a label and an entry for input the GFS resolution
text_GFSres = 'Select the GFS resolution (Type: 0p25, 0p50 or 1p00): '
GFSres_label, GFSres_entry =  setting_label_entry(root, text_GFSres, gfs_resolution)

# creating a label and an entry for input the days of prediction
text_days = 'How many days of prediction do you want? (Type a number): '
days_label, days_entry =  setting_label_entry(root, text_days, days_prediction)

# creating a button using the widget Button that will call the submit function  
sub_btn=tk.Button(root,text = 'Submit', command = submit)

text_authorlabel = 'Developed by Larissa de Freitas \nlarissafreita@gmail.com'
author_label = tk.Label(root, text = text_authorlabel, 
                        font = ('calibre',10,'bold'))

# Positioning the labels and entries using the grid method
root.title('Download GFS Data')
date_label.grid(row=0,column=0); date_entry.grid(row=0,column=1) 
hour_label.grid(row=1,column=0); hour_entry.grid(row=1,column=1) 
GFSres_label.grid(row=2,column=0); GFSres_entry.grid(row=2,column=1)
days_label.grid(row=3,column=0); days_entry.grid(row=3,column=1) 
sub_btn.grid(row=4,column=1) 
author_label.grid(row=10,column=1)
# performing an infinite loop  
# for the window to display 
root.mainloop() 

