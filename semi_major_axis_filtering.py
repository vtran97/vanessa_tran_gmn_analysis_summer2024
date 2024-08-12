'''
GMN datamining 

Vanessa Tran (vtran97@uwo.ca)
May 1st to August 16 (2024)

Filtering the semi major axis to see if there's a normal distribution around a particular a value
'''

# -----------------------------------------------------------------------------------------------------------
# imports - DO NOT DELETE!!!

# GMN
from gmn_python_api import data_directory as dd
from gmn_python_api import meteor_trajectory_reader

# graph
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

# get all months
from functions import get_all_months_by_year_list

# math
import math

plt.rcParams.update({'font.size':30})

# -----------------------------------------------------------------------------------------------------------
# dataminings starts here
# -----------------------------------------------------------------------------------------------------------

# data for all months
all_months = get_all_months_by_year_list()

def histogram_a_vals():
# if we're looking for multiple asteroid types, can create multiple lists :)

    counter = 0

    # lists to be reset for each year
    identifiers = []

    a_semi_major_axis = []
    eccentricity = []
    peri_argument = []
    ascending_node = []
    inclination = []
    rageo_asc = []
    decgeo_dec = []
    solar_longitude = []
    iau_codes = []

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
                i = traj_df['i (deg)'][ix]
                RAgeo = traj_df['RAgeo (deg)'][ix]
                Decgeo = traj_df['DECgeo (deg)'][ix]
                sol_lon = traj_df['Sol lon (deg)'][ix]
                iau = traj_df['IAU (code)'][ix]

                '''if node > 240 and node < 280 and a > -2 and a < 5:
                    a_semi_major_axis.append(a)
                    ascending_node.append(node)
                    eccentricity.append(e)
                    peri_argument.append(peri)
                '''
                
                #if a > 0.90 and a < 1.7 and node > 240 and node < 280:

                '''if a > 1.25 and a < 1.35 and \
                e > 0.85 and e < 0.95 and \
                i > 22.5 and i < 27.5 and \
                node > 257.5 and node < 262.5 and \
                peri > 317.5 and peri < 322.5 :'''
            
                identifiers.append(identity)
                #print(identity)
                a_semi_major_axis.append(a)
                #print(a)
                eccentricity.append(e)
                peri_argument.append(peri)
                ascending_node.append(node)
                inclination.append(i)
                #print(node)
                #print()
                rageo_asc.append(RAgeo)
                decgeo_dec.append(Decgeo)
                solar_longitude.append(sol_lon)
                counter += 1

                rupnode = a*(1-e**2)/(1+e*math.cos(-1 * math.radians(peri)))
                cross_point_asc_x = rupnode*math.cos(math.radians(node)) 
                cross_point_asc_y = rupnode*math.sin(math.radians(node))

                rdnnode = a*(1-e**2)/(1+e*math.cos(math.pi-math.radians(peri)))
                cross_point_des_x = rdnnode*math.cos(math.radians(node)+math.pi)
                cross_point_des_y = rdnnode*math.sin(math.radians(node)+math.pi)

                if cross_point_asc_x > -1.5 and cross_point_asc_x < 1.5 and cross_point_asc_y > -1.5 and cross_point_asc_y < 1.5 \
                    and cross_point_des_x > -1.5 and cross_point_des_x < 1.5 and cross_point_des_y > -1.5 and cross_point_des_y < 1.5 :
              
                    ascending_nodal_cross_point_list_x.append(cross_point_asc_x)
                    ascending_nodal_cross_point_list_y.append(cross_point_asc_y)
                    descending_nodal_cross_point_list_x.append(cross_point_des_x)
                    descending_nodal_cross_point_list_y.append(cross_point_des_y)
                    '''if str(iau) == "GEM":
                        iau_codes.append(1)
                    else:
                        iau_codes.append(0)'''
            
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
    '''
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

    plt.hist2d(ascending_node, inclination, bins=100, cmin=1)
    plt.colorbar()
    plt.title("i vs node")
    plt.xlabel('node')
    plt.ylabel('i')
    plt.grid()
    plt.show()
    '''
    
    import matplotlib

    plt.hist2d(ascending_nodal_cross_point_list_x, ascending_nodal_cross_point_list_y, bins=100, cmin=1, 
               norm=matplotlib.colors.LogNorm())
    plt.colorbar()
    plt.title("Nodal Footprint - ascending")
    plt.grid()
    plt.show()

    plt.hist2d(descending_nodal_cross_point_list_x, descending_nodal_cross_point_list_y, bins=100, cmin=1, 
               norm=matplotlib.colors.LogNorm())
    plt.colorbar()
    plt.title("Nodal Footprint - descending")
    plt.grid()
    plt.show()

    plt.scatter(ascending_nodal_cross_point_list_x, ascending_nodal_cross_point_list_y, c=iau_codes)
    plt.title("Nodal Footprint - ascending")
    plt.legend()
    plt.grid()
    plt.show()

    plt.scatter(descending_nodal_cross_point_list_x, descending_nodal_cross_point_list_y, c=iau_codes)
    plt.title("Nodal Footprint - descending")
    plt.legend()
    plt.grid()
    plt.show()

    print("# meteors:", counter)
    #print("identities list:", identifiers)

    plt.scatter(rageo_asc, decgeo_dec)
    plt.title("dec vs ra")
    plt.xlabel('rageo asc')
    plt.ylabel('decgeo dec')
    plt.grid()
    plt.show()

    plt.hist2d(rageo_asc, decgeo_dec, bins=100, cmin=1)
    plt.colorbar()
    plt.title("dec vs ra")
    plt.xlabel('rageo asc')
    plt.ylabel('decgeo dec')
    plt.grid()
    plt.show()

    plt.hist(solar_longitude)
    plt.title("Solar Longitude")
    plt.xlabel('sol lon')
    plt.ylabel('# of meteors')
    plt.grid()
    plt.show()

# activate
get_hist = histogram_a_vals()