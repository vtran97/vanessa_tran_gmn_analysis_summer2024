'''
GMN datamining 

Vanessa Tran (vtran97@uwo.ca)
May 1st to August 16 (2024)

This file searches through the entire GMN database and searches for potential interstellar meteors
with following conditions:
    - vhel > 42
    - error bars (vhel - sigma vhel) > 42
    - vinit below a specified threshold
    - vhel above a certain threshold (further narrowing)
    - sort by Qc (convergence)

Conditions arguments can be inputted to narrow/broaden the search. print statements separate and optional.
'''

# -----------------------------------------------------------------------------------------------------------
# imports - DO NOT DELETE!!!

# graphing
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import mpl_scatter_density # adds projection='scatter_density' 
import numpy as np
from scipy.stats import gaussian_kde

# GMN
from gmn_python_api import data_directory as dd
from gmn_python_api import meteor_trajectory_reader

# getting dates
from datetime import datetime

# -----------------------------------------------------------------------------------------------------------
# color map  for graphs

# "Viridis-like" colormap with white background (otherwise purple)
white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
    (0, '#ffffff'),
    (1e-20, '#440053'),
    (0.2, '#404388'),
    (0.4, '#2a788e'),
    (0.6, '#21a784'),
    (0.8, '#78d151'),
    (1, '#fde624'),
], N=256)

# -----------------------------------------------------------------------------------------------------------
# function : get all entries up to the current month 
# this helps to automatically create a list of all the years in the system so that
# you don't have to loop through them all manually (done by just making a bunch of lists and putting them
# into one at the end, but long term this is not effective)

def get_all_months_by_year_list():
    # returns a list of all months that the GMN has been active -- used to acccess data through GMN database

    # beginning of all data of GMN
    year = 2018

    all_months = []

    # Get the current mo
    x = str(datetime.now().date()).split("-")
    current_month = x[0] + "-" + x[1] 
    year_list = []
    start = "2018-12"
    current_month 

    for year in range(int(start.split("-")[0]), int(current_month.split("-")[0]) + 1):
        year_list.append(year)

    for year_no in range(len(year_list)):

        # this just allows the computer see the correct year instead of using index
        year = year_no + 2018

        if year == 2018:
            # special case, only one month and should never change (unless we build a time machine)
            all_months.append(['2018-12'])

        else:
            # for all months after leading up to current date for the current year 

            year_month_list = [] # full list
            cut_list = [] # list for the cut off year
            done = False # used for later for cut list

            for month in range(1, 13):

                if month in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    month_name = str(year) + '-0' + str(month)
                    year_month_list.append(month_name)

                else: # months 10, 11, 12
                    month_name = str(year) + "-" + str(month)
                    year_month_list.append(month_name)
            
            if year != int(current_month.split("-")[0]): # if the year is not the current year
                all_months.append(year_month_list)
            
            else: # if the year is the current year
                # need to shorten the lsit to find the months up to this point that we can analyse 
                # (not getting results from the future)

                while not done:
                    for i in range(len(year_month_list)):
                        if year_month_list[i] == current_month:
                            cut_list.append(year_month_list[i])
                            done = True
                        if year_month_list[i] != current_month and done == False:
                            cut_list.append(year_month_list[i])

                all_months.append(cut_list)

    # return list in form [[months from 2018], [months from 2019], [months from 2020], etc...]
    return all_months

# -----------------------------------------------------------------------------------------------------------
# function : printing output in python - can be edited to show more 

def print_output(value=0, value_cutoff=5, 
                 vhel=0, vhel_cutoff=50, 
                 vhel_sigma=0, 
                 vinit=0, vinit_cutoff=50, 
                 qc=0, 
                 identifier="", 
                 stations='', 
                 skyfit_script_identifier=''):
    
    # length for the text splits
    cus_lens = [8,6]
    res = []
    start = 0

    # prints the output give the above parameters
    output = ""
    if value > value_cutoff and vhel > vhel_cutoff and vinit < vinit_cutoff:

        ''' 
        # not needed right now -- modified to never have sigma = 0 entries 
        if vhel_sigma_mod[number] == 0:
            output += "||SIGMA = ZERO|| "
        else:
            output += "                 "
        '''

        output += "||IDENTITY: " + str(identifier) + "|| "

        txt = str(vhel)
        if len(txt) <= 7: # strings too short
            while len(txt) != 7:
                txt = txt + '0'
        output += "||VHEL: " + txt + "|| "

        if vhel_sigma != 0:
            txt = str(vhel_sigma)
            if len(txt) != 6:
                while len(txt) != 6:
                    txt += '0'
            output += "||SIGMA (VHEL): " + txt + "|| "
        
        txt = str(qc)
        if len(txt) <= 5:
            while len(txt) != 5:
                txt = txt + '0'
        output += "||QC: " + txt + "|| "

        txt = str(value)
        if len(txt) <= 18:
            while len(txt) != 18:
                txt = txt + '0'
        output += "||VALUE: " + txt + "|| "

        iden = str(identifier).split("_")[0]
        for size in cus_lens:
            res.append(iden[start : start + size])
            start += size

        txt = str(skyfit_script_identifier)
        txt = txt.split(".")[1]
        out = "\n\t\t||SCRIPT IDENTIFIER FOR RAW: " + res[0] + "_" + res[1] + "." + txt + "|| "
        output += out

        txt = ''
        last = len(stations) - 1
        for station in range(len(stations)): 
            if stations[station] != stations[last]:
                txt += stations[station] + ", "
            else:
                txt += stations[station]
        output += "||STATIONS: " + txt + "|| "

        print(output)

# -----------------------------------------------------------------------------------------------------------
# function : checking conditions

def check_conditions(value, value_cutoff,
                     vhel, vhel_cutoff, 
                     vhel_sigma,
                     vinit, vinit_cutoff):
    if value > value_cutoff and vhel_sigma !=0 and vhel > vhel_cutoff and vinit < vinit_cutoff:
        return True
    else:
        return False

# -----------------------------------------------------------------------------------------------------------
# DATAMINING BEGINS HERE
# -----------------------------------------------------------------------------------------------------------

# calling function 
all_months = get_all_months_by_year_list()

# system lists for whichever parameters we decide to edit 
system_identifiers = []
system_vinit = []
system_calc = []
system_qc = []
system_stations = []
system_skyfit_script_identifiers = []

# looping through all years
for month_list in all_months:

    year = month_list[0].split("-")[0]

    print(f"\n************\nYEAR : {year}\n************")

    # lists to be reste for each year :D
    calculation_best_data =  []
    vinit_best_data_for_plot = []
    best_data_identifiers = []
    best_qc = []
    best_stations = []
    best_skyfit_script_identifiers = []

    # looping through each month in the year
    for month in month_list:

        # Analyse recorded meteor data monthly 
        traj_file_content = dd.get_monthly_file_content_by_date(month)

        # Read data as a Pandas DataFrame
        traj_df = meteor_trajectory_reader.read_data(traj_file_content)

        # all lists 
        identifiers = []
        vhel_larger_than_42 = []
        vhel_sigma = []
        vinit = []
        vinit_sigma = []
        qc = []
        stations = []
        skyfit_script_identifiers = []

        # iterating through the traj_df using vhel 
        index = 0
        for vhel in traj_df['Vhel (km/s)']:

            # get only entries with these conditions
            if vhel > 42 and vhel - traj_df['+/- (sigma.7)'][index] > 42:

                # identifiers
                identifiers.append(traj_df.index[index])
                
                # vhel 
                vhel_larger_than_42.append(vhel)

                # vhel sigma 
                vhel_sigma.append(traj_df['+/- (sigma.7)'][index])

                # vinit
                vinit.append(traj_df['Vinit (km/s)'][index])

                # vinit sigma 
                vinit_sigma.append(traj_df['+/- (sigma.26)'][index])

                # qc
                qc.append(traj_df['Qc (deg)'][index])

                # stations
                stations.append(traj_df['Participating (stations)'][index])

                # script skyfit identifers
                skyfit_script_identifiers.append(traj_df['Beginning (UTC Time)'][index])

            index += 1

        # -----------------------------------------------------------------------------------------------------------
        # narrowing conditions and getting data 

        # ADJUST NARROWED CONDITIONS HERE! 
        # conditions = value, vhel, vinit
        conditions = [5, 49.6, 50]

        for number in range(len(vhel_larger_than_42)):
            value = (vhel_larger_than_42[number] - 42) / vhel_sigma[number]
            # (vhel-42) / sigma vhel as a measurement (y axis) 
                # it is a ratio to see how many errors bars above 42 that meteor is (vhel)

            # getting only the best data with inputted conditions (see conditions above)
            if check_conditions(value, conditions[0],
                    vhel_larger_than_42[number], conditions[1],
                    vhel_sigma[number], 
                    vinit[number], conditions[2]) : # this will return True or False
                
                # appending to lists
                calculation_best_data.append(value)
                vinit_best_data_for_plot.append(vinit[number])
                best_data_identifiers.append(identifiers[number])
                best_qc.append(qc[number])
                best_stations.append(stations[number])
                best_skyfit_script_identifiers.append(skyfit_script_identifiers[number])

            # printing in output for the conditions specified -- separate from the appending conditions
            output = ""
            print_output(value, conditions[0],
                         vhel_larger_than_42[number], conditions[1], 
                         vhel_sigma[number], 
                         vinit[number], conditions[2],
                         qc[number], 
                         identifiers[number], 
                         stations[number], 
                         skyfit_script_identifiers[number])

    '''
    # YEARLY GRAPHS
    plt.errorbar(vinit_best_data_for_plot, calculation_best_data_greater_than_50, 0, 0, 'x')

    # helps with scale
    plt.axhline(50, c='green')
    plt.axhline(200, c='blue')
    plt.axhline(5, c='red')

    plt.title(f'{year} : [(vhel - 42) / sigma] vs vinit (km/s)')
    plt.ylabel('[(vhel - 42) / sigma]')
    plt.xlabel('vinit (km/s)')

    plt.grid()
    plt.show()
    '''

    # adding to the system lists --> final lists for the final graphs at the end since this info is all by year
    system_identifiers += best_data_identifiers
    system_vinit += vinit_best_data_for_plot
    system_calc += calculation_best_data
    system_qc += best_qc
    system_stations += best_stations
    system_skyfit_script_identifiers += best_skyfit_script_identifiers

# -----------------------------------------------------------------------------------------------------------
# SYSTEM GRAPH - NORMAL SCATTERPLOT
'''
plt.scatter(system_vinit, system_calc)  

plt.axhline(50, c='green')
plt.axhline(200, c='blue')
plt.axhline(5, c='red')

plt.title(f'ALL YEARS : [(vhel - 42) / sigma] vs vinit (km/s)')
plt.ylabel('[(vhel - 42) / sigma]')
plt.xlabel('vinit (km/s)')

plt.show()
'''
# -----------------------------------------------------------------------------------------------------------
# GRAPH SORTED BY QC

# creating pandas dataframe so that we can colour-code according to a third variable and identify using a fourth 
d = {'Vinit (km/s)'          : tuple(system_vinit), 
     '[(vhel - 42) / sigma]' : tuple(system_calc), 
     'Qc (deg)'              : tuple(system_qc),
     'Identifiers'           : tuple(system_identifiers)}
dataframe = pd.DataFrame(d)

#c creating plot
ax = dataframe.plot.scatter(x='Vinit (km/s)', y='[(vhel - 42) / sigma]', 
                            c='Qc (deg)', colormap='viridis', 
                            title="ALL YEARS : [(vhel - 42) / sigma] vs vinit (km/s)")

# if we wanted to annotate the points with anything - identifiers for now
for idx, row in dataframe.iterrows():
    ax.annotate(row['Identifiers'], (row['Vinit (km/s)'], row['[(vhel - 42) / sigma]']), 
                xytext=(-60,10), textcoords='offset points')

plt.grid()
plt.show()

# -----------------------------------------------------------------------------------------------------------
# DENSITY MAP
'''
def using_mpl_scatter_density(fig, x, y):
    ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
    density = ax.scatter_density(x, y, cmap=white_viridis)
    fig.colorbar(density, label='Number of points per pixel')

fig = plt.figure()
using_mpl_scatter_density(fig, system_vinit, system_calc)
plt.show()
'''

# -----------------------------------------------------------------------------------------------------------
# 2D HISTOGRAM
'''
plt.hist2d(system_vinit, system_calc, (200, 100), cmap=plt.cm.viridis, cmin=1)
plt.title(f'ALL YEARS : [(vhel - 42) / sigma] vs vinit (km/s)')
plt.ylabel('[(vhel - 42) / sigma]')
plt.xlabel('vinit (km/s)')
cbr = plt.colorbar()
cbr.set_label("# of error bars above 42 km/s")
plt.show()
'''

# -----------------------------------------------------------------------------------------------------------
# GAUSSIAN PLOT - NOT SORTED
'''
# data
x = system_vinit
y = system_calc

# Calculate the point density
xy = np.vstack([x,y])
z = gaussian_kde(xy)(xy)

fig, ax = plt.subplots()
cax = ax.scatter(x, y, c=z, s=100)
fig.colorbar(cax)
plt.show()
'''
