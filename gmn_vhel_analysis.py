'''
GMN datamining :)

Vanessa Tran (vtran97@uwo.ca)
May 1st to August 16 (2024)
'''

# -----------------------------------------------------------------------------------------------------------
# imports - DO NOT DELETE!!!

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import mpl_scatter_density # adds projection='scatter_density' 

import numpy as np

from gmn_python_api import data_directory as dd
from gmn_python_api import meteor_trajectory_reader

from datetime import datetime

# -----------------------------------------------------------------------------------------------------------
# color map 

# "Viridis-like" colormap with white background
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
# get all entries up to the current month 
# this helps to automatically create a list of all the years in the system so that
# you don't have to loop through them all manually

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
        # special case, only one month 
        all_months.append(['2018-12'])

    elif year == int(current_month.split("-")[0]):
        # for all months after leading up to current date for the current year 

        year_month_list = [] # full list
        cut_list = [] # list for the cut off year
        done = False

        for month in range(1, 13):

            if month in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                month_name = str(year) + '-0' + str(month)
                year_month_list.append(month_name)

            else: # months 10, 11, 12
                month_name = str(year) + "-" + str(month)
                year_month_list.append(month_name)

        while not done:

            for i in range(len(year_month_list)):
                # print(year_month_list[i])
                if year_month_list[i] == current_month:
                    cut_list.append(year_month_list[i])
                    done = True
                if year_month_list[i] != current_month and done == False:
                    cut_list.append(year_month_list[i])

        all_months.append(cut_list)

    else: # year is not start or end year

        year_month_list = [] # full list (works for full year)

        for month in range(1, 13):

            if month in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                month_name = str(year) + '-0' + str(month)
                year_month_list.append(month_name)

            else: # months 10, 11, 12
                month_name = str(year) + "-" + str(month)
                year_month_list.append(month_name)

        all_months.append(year_month_list)

# -----------------------------------------------------------------------------------------------------------
# datamining begins here

# system lists for whichever parameters we decide to edit 
system_best_identifiers = []
system_vinit = []
system_calc = []
system_qc = []

# for looping through all the years an displaying what year it is in python print --> kinda jank but it is what it is 
year = 2018

for month_list in all_months:

    print("\n************")
    print(f"YEAR : {year}")
    print("************")

    # lists to be reste for each year :D
    calculation_best_data_greater_than_50 =  []
    vinit_best_data_for_plot = []
    best_data_identifiers = []
    best_qc = []

    for month in month_list:

        # Analyse recorded meteor data monthly 
        traj_file_content = dd.get_monthly_file_content_by_date(month)

        # Read data as a Pandas DataFrame
        traj_df = meteor_trajectory_reader.read_data(traj_file_content)

        # all lists 
        identifiers = []
        vhel_larger_than42 = []
        vhel_sigma = []
        vhel_var = []
        vinit = []
        vinit_sigma = []
        vinit_var = []
        qc = []

        # iterating through the traj_df using vhel 
        index = 0
        for vhel in traj_df['Vhel (km/s)']:

            if vhel > 42:

                # identifiers
                identifiers.append(traj_df.index[index])
                
                # vhel 
                vhel_larger_than42.append(vhel)

                # vhel sigma 
                vhel_sigma.append(traj_df['+/- (sigma.7)'][index])

                # vinit
                vinit.append(traj_df['Vinit (km/s)'][index])

                # vinit sigma 
                vinit_sigma.append(traj_df['+/- (sigma.26)'][index])

                # qc
                qc.append(traj_df['Qc (deg)'][index])

            index += 1

        # -----------------------------------------------------------------------------------------------------------
        # creating scatterplots
        
        # ( sigma_vhel / (vhel-42) ) vs vhel 
        # sorting by seeing which have the largest and smallest errors with greatest vhel 

        identity_vhel_larger_than_42_and_errbars_above_42 = []
        vhel_larger_than_42_and_errbars_above_42 = []
        vhel_sigma_mod = [] # mod = modified
        vinit_mod = []
        vinit_sigma_mod = []
        qc_mod = []

        # checking if error bars are above 42 as base (increased filtering)
        for j in range(len(vhel_larger_than42)):
            if vhel_larger_than42[j] - vhel_sigma[j] > 42 :

                # idenitites 
                identity_vhel_larger_than_42_and_errbars_above_42.append(identifiers[j])
                
                # vhel + sigma
                vhel_larger_than_42_and_errbars_above_42.append(vhel_larger_than42[j])
                vhel_sigma_mod.append(vhel_sigma[j])
                
                # vinit + sigma 
                vinit_mod.append(vinit[j])
                vinit_sigma_mod.append(vinit_sigma[j])

                # qc
                qc_mod.append(qc[j])

        '''
        # MONTHLY GRAPH - ONLY VERTICAL ERROR BARS (no horizontal)
        plt.errorbar(vinit_mod, vhel_larger_than_42_and_errbars_above_42, vhel_sigma_mod, 0, 'x', 'red')

        plt.axhline(42, c='green')

        plt.title(f'vhel (km/s) vs vinit (km/s) for {month}')
        plt.ylabel('vhel (km/s)')
        plt.xlabel('vinit (km/s)')

        plt.show()
        '''
        # (vhel-42) / sigma vhel as a measurement (y axis) --> this can be merged to clean up the code, but is separate for now 
        # it is a ratio to see ho many errors bars above 42 that meteor is (vhel)

        computation = []

        for number in range(len(vhel_larger_than_42_and_errbars_above_42)):
            value = (vhel_larger_than_42_and_errbars_above_42[number] - 42) / vhel_sigma_mod[number]
            computation.append(value)

            # getting only the best data (list outside loop) MODIFIED TO GET ONLY NON-0 ENTRIES AND VHEL > 50, VINIT < 50
            if value > 5 and vhel_sigma_mod[number] != 0 and vhel_larger_than_42_and_errbars_above_42[number] > 50 and vinit_mod[number] < 50 :
                calculation_best_data_greater_than_50.append(value)
                vinit_best_data_for_plot.append(vinit_mod[number])
                best_data_identifiers.append(identity_vhel_larger_than_42_and_errbars_above_42[number])
                best_qc.append(qc_mod[number])

            # OUTPUT - modifiable 
            output = ""
            if value > 5 and vhel_larger_than_42_and_errbars_above_42[number] > 50 and vinit_mod[number] < 50:

                ''' 
                # not needed right now -- modified to never have sigma = 0 entries 
                if vhel_sigma_mod[number] == 0:
                    output += "||SIGMA = ZERO|| "
                else:
                    output += "                 "
                '''

                output += "||IDENTITY: " + str(identity_vhel_larger_than_42_and_errbars_above_42[number]) + "|| "

                if len(str(vhel_larger_than_42_and_errbars_above_42[number])) == 7:
                    text = str(vhel_larger_than_42_and_errbars_above_42[number]) + '0'
                    output += "||SPEED (VHEL): " + text + "|| "
                else: 
                    output += "||SPEED (VHEL): " + str(vhel_larger_than_42_and_errbars_above_42[number]) + "|| "

                if vhel_sigma_mod[number] != 0:
                    txt = str(vhel_sigma_mod[number])
                    if len(txt) != 6:
                        while len(txt) != 6:
                            txt += '0'
                    output += "||SIGMA (VHEL): " + txt + "|| "

                output += "||QC: " + str(qc_mod[number]) + "|| "

                output += "||VALUE: " + str(value) + "||"

                print(output)

        '''
        # MONTHLY GRAPHS
        plt.errorbar(vinit_mod, computation, 0, 0, 'x')

        plt.axhline(5, c='green')
        plt.title(f'[(vhel - 42) / sigma] vs vinit (km/s) {month}')
        plt.ylabel('[(vhel - 42) / sigma]')
        plt.xlabel('vinit (km/s)')

        plt.show()
        '''
    '''
    # YEARLY GRAPHS
    plt.errorbar(vinit_best_data_for_plot, calculation_best_data_greater_than_50, 0, 0, 'x')

    plt.axhline(50, c='green')
    plt.axhline(200, c='blue')
    plt.axhline(5, c='red')
    plt.title(f'{year} : [(vhel - 42) / sigma] vs vinit (km/s)')
    plt.ylabel('[(vhel - 42) / sigma]')
    plt.xlabel('vinit (km/s)')

    plt.show()
    '''

    # adding to the system lists --> final lists for the final graphs at the end
    system_best_identifiers += best_data_identifiers
    system_vinit += vinit_best_data_for_plot
    system_calc += calculation_best_data_greater_than_50
    system_qc += best_qc
    
    # updating year
    year += 1

# -----------------------------------------------------------------------------------------------------------
'''
# SYSTEM GRAPH - SCATTERPLOT
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

d = {'Vinit (km/s)'           : tuple(system_vinit), 
     '[(vhel - 42) / sigma]'  : tuple(system_calc), 
     'Qc (deg)'               : tuple(system_qc)}
dataframe = pd.DataFrame(d)

dataframe.plot.scatter('Vinit (km/s)', '[(vhel - 42) / sigma]', c='Qc (deg)', 
                        colormap='viridis', title="ALL YEARS : [(vhel - 42) / sigma] vs vinit (km/s)")
plt.show()

# -----------------------------------------------------------------------------------------------------------
'''
# density map
def using_mpl_scatter_density(fig, x, y):
    ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
    density = ax.scatter_density(x, y, cmap=white_viridis)
    fig.colorbar(density, label='Number of points per pixel')

fig = plt.figure()
using_mpl_scatter_density(fig, system_vinit, system_calc)
plt.show()

# 2d hist
plt.hist2d(system_vinit, system_calc, (200, 100), cmap=plt.cm.viridis, cmin=1)
plt.title(f'ALL YEARS : [(vhel - 42) / sigma] vs vinit (km/s)')
plt.ylabel('[(vhel - 42) / sigma]')
plt.xlabel('vinit (km/s)')
cbr = plt.colorbar()
cbr.set_label("# of error bars above 42 km/s")
plt.show()
'''
# -----------------------------------------------------------------------------------------------------------
'''
# gaussian plot sorted
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Generate fake data
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
