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
    eccentricity = []
    peri_argument = []
    ascending_node = []

    ascending_nodal_cross_point_list_x = []
    ascending_nodal_cross_point_list_y = []
    descending_nodal_cross_point_list_x = []
    descending_nodal_cross_point_list_y = []

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
                e = traj_df['e'][ix]
                peri = traj_df['peri (deg)'][ix]
                node = traj_df['node (deg)'][ix]

                '''if node > 240 and node < 280 and a > -2 and a < 5:
                    a_semi_major_axis.append(a)
                    ascending_node.append(node)
                    eccentricity.append(e)
                    peri_argument.append(peri)
                '''
                
                if a > 0.90 and a < 1.7 and node > 240 and node < 280:
                    
                    identifiers.append(identity)
                    #print(identity)
                    a_semi_major_axis.append(a)
                    #print(a)
                    eccentricity.append(e)
                    peri_argument.append(peri)
                    ascending_node.append(node)
                    #print(node)
                    #print()

                    rupnode = a*(1-e**2)/(1+e*math.cos(-1 *peri))
                    cross_point_asc_x = rupnode*math.cos(node) 
                    cross_point_asc_y = rupnode*math.sin(node)
                    ascending_nodal_cross_point_list_x.append(cross_point_asc_x)
                    ascending_nodal_cross_point_list_y.append(cross_point_asc_y)

                    rdnnode = a*(1-e**2)/(1+e*math.cos(math.pi-peri))
                    cross_point_des_x = rdnnode*math.cos(node+math.pi)
                    cross_point_des_y = rdnnode*math.sin(node+math.pi)

                    descending_nodal_cross_point_list_x.append(cross_point_des_x)
                    descending_nodal_cross_point_list_y.append(cross_point_des_y)
                
    '''plt.hist(a_semi_major_axis, bins=[0.98, 0.9825, 0.9850, 0.9875, 
                                      0.99, 0.9925, 0.9950, 0.9975,
                                      1.00, 1.0025, 1.0050, 1.0075, 
                                      1.01, 1.0125, 1.0150, 1.0175,
                                      1.02])
    plt.title("Semi major axis histogram")
    plt.xlabel('a')
    plt.ylabel('# of meteors')
    plt.grid()
    plt.show()'''

    plt.scatter(a_semi_major_axis, ascending_node)
    plt.title("node vs a")
    plt.xlabel('a')
    plt.ylabel('node')
    plt.grid()
    plt.show()

    plt.hist(ascending_node, bins=36)
    plt.title("node histogram")
    plt.xlabel('node')
    plt.ylabel('# of meteors')
    plt.grid()
    plt.show()

    plt.hist2d(ascending_node, a_semi_major_axis, bins=100, cmin=1)
    plt.colorbar()
    plt.title("a vs node")
    plt.ylabel('a')
    plt.xlabel('node')
    plt.grid()
    plt.show()


    plt.hist2d(ascending_node, eccentricity, bins=100, cmin=1)
    plt.colorbar()
    plt.title("e vs node")
    plt.xlabel('node')
    plt.ylabel('e')
    plt.grid()
    plt.show()

    plt.hist2d(ascending_node, peri_argument, bins=100, cmin=1)
    plt.colorbar()
    plt.title("peri vs node")
    plt.xlabel('node')
    plt.ylabel('peri')
    plt.grid()
    plt.show()

    plt.hist2d(ascending_nodal_cross_point_list_x, ascending_nodal_cross_point_list_y, bins=100, cmin=1)
    plt.colorbar()
    plt.title("Nodal Footprint - ascending")
    plt.grid()
    plt.show()

    plt.hist2d(descending_nodal_cross_point_list_x, descending_nodal_cross_point_list_y, bins=100, cmin=1)
    plt.colorbar()
    plt.title("Nodal Footprint - descending")
    plt.grid()
    plt.show()
    
get_hist = histogram_a_vals()