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

See "How-To : Access files for GMN for Datamining" in References in GitHub
See Interstellar Reductions Stats (xlsx)
See Potential Interstellars (xslx)
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

# get all months
from functions import get_all_months_by_year_list, check_conditions_interstellar, \
print_output_interstellar, camextract_mobaX, get_pickletraj_mobaX

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
# DATAMINING BEGINS HERE
# -----------------------------------------------------------------------------------------------------------

# using file to write all outputs
'''file = open("fullform_43-44.txt", "w")
file_camextract_mobaX = open("camextract_mobaX_43-44.txt", "w")
file_get_pickletraj_mobaX = open("get_pickletraj_mobaX_43-44.txt", "w")'''

# calling function 
all_months = get_all_months_by_year_list()

# system lists --> all years (separated by month and by year inside)
system_identifiers = []
system_vinit = []
system_vhel = []
system_vgeo = []
system_calc = []
system_qc = []
system_stations = []
system_skyfit_script_identifiers = []
system_b_ht = []

counter = 0

# looping through all years
for month_list in all_months:

    year = month_list[0].split("-")[0]

    print(f"\n************\nYEAR : {year}\n************")

    # lists to be reset for each year
    calculation_best_data =  []
    vinit_best_data_for_plot = []
    vhel_best_data_for_plot = []
    vgeo_best_data_for_plot = []
    best_data_identifiers = []
    best_qc = []
    best_stations = []
    best_skyfit_script_identifiers = []
    best_beg_heights = []

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
        vgeo = []
        vgeo_sigma = []
        qc = []
        stations = []
        skyfit_script_identifiers = []
        beg_heights = []

        # iterating through the traj_df using vhel 
        index = 0
        for vhel in traj_df['Vhel (km/s)']:
            # print("vhel", vhel)

            # get only entries with vhel > 42 and vhel minus one error bar is still larger than 42

            # NOTE : ADDED ANOTHER REQUIREMENT FOR NUMBER OF CAMERAS = 3+ FOR SOLN

            if vhel > 42 and vhel - traj_df['+/- (sigma.7)'][index] > 42 and traj_df['Num (stat)'][index] > 2 \
                and traj_df['IAU (No)'][index] == -1:

                # identifiers
                identifiers.append(traj_df.index[index])

                # vgeo
                vgeo.append(traj_df['Vgeo (km/s)'][index])

                # vgeo sigma
                vgeo_sigma.append(traj_df['+/- (sigma.4)'][index])
                
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

                # beginnning heights
                beg_heights.append(traj_df['HtBeg (km)'][index])

            index += 1

        # -----------------------------------------------------------------------------------------------------------
        # narrowing conditions and getting data 

        # ADJUST NARROWED CONDITIONS HERE! 
        # conditions = calc value min, vhel min (defualt 42 already due to the conditions anyway), vinit max, vhel max
        conditions = [0, 40, 100, 100]

        for number in range(len(vhel_larger_than_42)):
            value = 0
            if vhel_sigma[number] != 0:
                value = (vhel_larger_than_42[number] - 42) / vhel_sigma[number]
            else:
                value = 999999999999999999999.0
            # (vhel-42) / sigma vhel as a measurement (y axis) 
                # it is a ratio to see how many errors bars above 42 that meteor is (vhel)

            # getting only the best data with inputted conditions (see conditions above)
            if check_conditions_interstellar(value, conditions[0],
                    vhel_larger_than_42[number], conditions[1],
                    vhel_sigma[number], 
                    vinit[number], conditions[2]) \
                    and qc[number] > 20 \
                    and beg_heights[number] > 50 \
                    and beg_heights[number] < 150 \
                    and vhel_larger_than_42[number] < conditions[3]: 
                    # original heights : 95. 120 --> paper 50 < height < 150

                # appending to lists
                calculation_best_data.append(value)
                vgeo_best_data_for_plot.append(vgeo[number])
                vhel_best_data_for_plot.append(vhel_larger_than_42[number])
                vinit_best_data_for_plot.append(vinit[number])
                best_data_identifiers.append(identifiers[number])
                best_qc.append(qc[number])
                best_stations.append(stations[number])
                best_skyfit_script_identifiers.append(skyfit_script_identifiers[number])

                # printing in output for the conditions specified -- separate from the appending conditions
                output = ""
                '''print(print_output_interstellar(value, conditions[0],
                         vgeo[number],
                         vhel_larger_than_42[number], conditions[1], 
                         vhel_sigma[number], 
                         vinit[number], conditions[2],
                         qc[number], 
                         identifiers[number], 
                         stations[number], 
                         skyfit_script_identifiers[number]))'''
                '''file.write(print_output_interstellar(value, conditions[0],
                         vgeo[number],
                         vhel_larger_than_42[number], conditions[1], 
                         vhel_sigma[number], 
                         vinit[number], conditions[2],
                         qc[number], 
                         identifiers[number], 
                         stations[number], 
                         skyfit_script_identifiers[number])+"\n")
                file_camextract_mobaX.write(camextract_mobaX(identifiers[number], 
                         stations[number], 
                         skyfit_script_identifiers[number]))
                file_get_pickletraj_mobaX.write(get_pickletraj_mobaX("C:/Users/vtran97/GMN_GRAPH_DATA/vhel_42_43_CAMFILES", 
                         identifiers[number], 
                         stations[number], 
                         skyfit_script_identifiers[number]))'''
                
                counter += 1

        # monthly graphs ? 
        # plt.errorbar(vhel_larger_than_42, vgeo, vgeo_sigma, vhel_sigma, 'x', ecolor='red')
        '''plt.rcParams.update({'font.size':20})
        plt.errorbar(vgeo, vhel_larger_than_42, vhel_sigma, vgeo_sigma, 'x', ecolor='red')
        plt.title(f'{year}/{month} : vgeo (km/s) vs vhel (km/s)')
        plt.ylabel('vhel (km/s)')
        plt.xlabel('vgeo (km/s)')
        plt.grid()
        plt.show()'''

    # YEARLY GRAPHS
    '''plt.errorbar(vhel_larger_than_42, vgeo, vgeo_sigma, vhel_sigma, 'x', ecolor='blue')

    # helps with scale
    plt.axhline(50, c='green')
    plt.axhline(200, c='blue')
    plt.axhline(5, c='red')

    plt.title(f'{year} : vgeo (km/s) vs vhel (km/s)')
    plt.ylabel('vgeo (km/s)')
    plt.xlabel('vhel (km/s)')

    plt.grid()
    plt.show()'''

    # adding to the system lists --> final lists for the final graphs at the end since this info is all by year
    system_identifiers += best_data_identifiers
    system_vhel += vhel_best_data_for_plot
    system_vinit += vinit_best_data_for_plot
    system_vgeo += vgeo_best_data_for_plot
    system_calc += calculation_best_data
    system_qc += best_qc
    system_stations += best_stations
    system_skyfit_script_identifiers += best_skyfit_script_identifiers

'''file.close()
file_camextract_mobaX.close()
file_get_pickletraj_mobaX.close()'''

# -----------------------------------------------------------------------------------------------------------
# SYSTEM GRAPH - NORMAL SCATTERPLOT

plt.scatter(system_vhel, system_vgeo, marker='x')  

plt.axhline(50, c='purple')
plt.axvline(42, c='red')
plt.axvline(43, c='orange')
plt.axvline(44, c='yellow')
plt.axvline(45, c='green')
# plt.axhline(200, c='blue')
# plt.axhline(5, c='red')

plt.title(f'ALL YEARS : vgeo vs vinit (km/s)')
plt.ylabel('vgeo (km/s)')
plt.xlabel('vhel (km/s)')

plt.grid()
plt.show()

print(counter)

# -----------------------------------------------------------------------------------------------------------
# GRAPH SORTED BY QC

plt.rcParams.update({'font.size':30})

print(counter)

# creating pandas dataframe so that we can colour-code according to a third variable and identify using a fourth 
d = {'Vgeo (km/s)'       : tuple(system_vgeo), 
     '[(vhel - 42) / σ]' : tuple(system_calc), 
     'Vinit (km/s)'      : tuple(system_vinit),
     'Qc (deg)'          : tuple(system_qc),
     'Vhel (km/s)'       : tuple(system_vhel),
     'Identifiers'       : tuple(system_identifiers)
     }

dataframe = pd.DataFrame(d)


# creating plot using dataframe and ax
# c = colored by Qc
ax = dataframe.plot.scatter(x='Vhel (km/s)', y='[(vhel - 42) / σ]', 
                            c='Vgeo (km/s)', colormap='viridis', 
                            title="ALL YEARS : [(vhel - 42) / σ] vs Vhel (km/s)")

# annotate the points with anything - identifiers 
'''for idx, row in dataframe.iterrows():
    ax.annotate(row['Identifiers'], (row['Vgeo (km/s)'], row['[(vhel - 42) / σ]']), 
                xytext=(-60,10), textcoords='offset points')'''
'''ax.annotate(row['Identifiers'], (row['Vgeo (km/s)'], row['[(vhel - 42) / σ]']), 
                xytext=(-60,10), textcoords='offset points')'''

plt.grid()
plt.show()

ax = dataframe.plot.scatter(x='Vgeo (km/s)', y='Vinit (km/s)', 
                            c='Vhel (km/s)', colormap='viridis', 
                            title="ALL YEARS : Vinit vs Vgeo (km/s)")
x_val = list(system_vgeo)
y_val = list(system_vinit)
slope, intercept = np.polyfit(x_val, y_val, 1)
# line_of_best_fit = slope * x_val + intercept
equation_text = f'y = {slope:.2f}x + {intercept:.2f}'
plt.text(0.05, 0.95, equation_text, transform=plt.gca().transAxes, fontsize=12,
        verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', ec='k', lw=1, alpha=0.7))

# annotate the points with anything - identifiers 
'''for idx, row in dataframe.iterrows():
    ax.annotate(row['Identifiers'], (row['Vgeo (km/s)'], row['[(vhel - 42) / σ]']), 
                xytext=(-60,10), textcoords='offset points')'''
'''ax.annotate(row['Identifiers'], (row['Vgeo (km/s)'], row['[(vhel - 42) / σ]']), 
                xytext=(-60,10), textcoords='offset points')'''

plt.grid()
plt.show()

# -----------------------------------------------------------------------------------------------------------
# DENSITY MAP

def using_mpl_scatter_density(fig, x, y):
    ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
    density = ax.scatter_density(x, y, cmap=white_viridis)
    fig.colorbar(density, label='Number of points per pixel')

fig = plt.figure()
using_mpl_scatter_density(fig, system_vhel, system_vgeo)
plt.axhline(50, c='gray')
plt.axvline(42, c='pink')
plt.axvline(43, c='red')
plt.axvline(44, c='orange')
plt.axvline(45, c='yellow')
plt.title(f'ALL YEARS : vgeo vs vhel (km/s)')
plt.ylabel('vgeo (km/s)')
plt.xlabel('vhel (km/s)')
plt.grid()
plt.show()


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
