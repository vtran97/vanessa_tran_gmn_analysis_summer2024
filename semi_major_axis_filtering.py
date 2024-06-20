'''
GMN datamining 

Vanessa Tran (vtran97@uwo.ca)
May 1st to August 16 (2024)

Just filtering the semi major axis to see if there's a normal distribution (there isn't) 
'''

# -----------------------------------------------------------------------------------------------------------
# imports - DO NOT DELETE!!!

# GMN
from gmn_python_api import data_directory as dd
from gmn_python_api import meteor_trajectory_reader

# graph
import matplotlib.pyplot as plt
import pandas as pd

# get all months
from functions import get_all_months_by_year_list

# math
import math

# -----------------------------------------------------------------------------------------------------------
# dataminings starts here
# -----------------------------------------------------------------------------------------------------------

# data for all months
all_months = get_all_months_by_year_list()

def histogram_a_vals():
# if we're looking for multiple asteroid types, can create multiple lists :)

  # lists to be reset for each year
    identifiers = []

    a_semi_major_axis = []

    # looping through all year data
    for month_list in all_months:

        # looping through each month in the year
        for month in month_list:

            # Analyse recorded meteor data monthly 
            traj_file_content = dd.get_monthly_file_content_by_date(month)

            # Read data as a Pandas DataFrame
            traj_df = meteor_trajectory_reader.read_data(traj_file_content)
            
            for ix in range(len(traj_df['a (AU)'])):
                # get all information needde from the dataframe
                
                identity = traj_df.index[ix]

                a = traj_df['a (AU)'][ix]

                if a > 0.98 and a < 1.02:
                    
                    identifiers.append(identity)
                    a_semi_major_axis.append(a)

    plt.hist(a_semi_major_axis, bins=75)
    plt.title("Semi major axis histogram")
    plt.xlabel('a')
    plt.ylabel('# of meteors')
    plt.grid()
    plt.show()
    
get_hist = histogram_a_vals()