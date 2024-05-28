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

# get all months
from get_all_months import get_all_months_by_year_list

# for D values
from d_value_meteor_class import Meteor

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
# check conditions

def check_conditions(a, a_min, a_max, 
                     e, e_min, e_max, 
                     i, i_min, i_max,
                     peri, peri_min, peri_max,
                     node, node_min, node_max,
                     Pi, Pi_min, Pi_max,
                     b, b_min, b_max,
                     q, q_min, q_max,
                     f, f_min, f_max,
                     M, M_min, M_max,
                     Q, Q_min, Q_max,
                     n, n_min, n_max,
                     T, T_min, T_max,
                     TisserandJ, TisserandJ_min, TisserandJ_max):
    if a > a_min and a < a_max :
        if e > e_min and e < e_max: 
            if i_min < 0:
                # editing the restrictions isince i angle covers interval before and after Zero
                i_sub_min = 360 + i_min
                i_sub_max = 360
                # reset i min to 0 for interval 
                i_min = 0
                if i > i_min and i < i_max or i < i_sub_max and i > i_sub_min:
                    if peri > peri_min and peri < peri_max:
                        if node > node_min and node < node_max:
                            if Pi > Pi_min and Pi < Pi_max:
                                if b > b_min and b < b_max:
                                    if q > q_min and q < q_max:
                                        if f > f_min and f < f_max:
                                            if M > M_min and M < M_max:
                                                if Q > Q_min and Q < Q_max:
                                                    if n > n_min and n < n_max:
                                                        if T > T_min and T < T_max:
                                                            if TisserandJ > TisserandJ_min and TisserandJ < TisserandJ_max:
                                                                return True
    return False

# -----------------------------------------------------------------------------------------------------------
# dataminings starts here
# -----------------------------------------------------------------------------------------------------------

# data for all months
all_months = get_all_months_by_year_list()

# system lists 
system_identifiers = []

system_a_semi_major_axis = []
system_sigma_a_semi_major_axis = []

system_e_eccentricity = []
system_sigma_eccentricity = []

system_i_inclination = []
system_sigma_inclination = []

system_peri_argument = []
system_sigma_peri_argument = [] 

system_ascending_node = []
system_sigma_ascending_node = []

system_Pi_peri_longitude = []

system_b_peri_latitude = []

system_q_peri_distance = []

system_f_true_anomaly = []

system_M_mean_anomaly = []

system_Q_aphelion_dist = []

system_n_motion = []

system_T_orbital_period = []

system_TisserandJ = []

asteroid_obj_list = []

# loopig through all year data
for month_list in all_months:

    year = month_list[0].split("-")[0]

    print(f"\n************\nYEAR : {year}\n************")

    # lists to be reset for each year
    identifiers = []

    a_semi_major_axis = []
    sigma_a_semi_major_axis = []

    eccentricity = []
    sigma_eccentricity = []

    inclination = []
    sigma_inclination = []

    peri_argument = []
    sigma_peri_argument = []

    ascending_node = []
    sigma_ascending_node = []

    Pi_peri_longitude = []

    b_peri_latitude = []

    q_peri_distance = []

    f_true_anomaly = []

    M_mean_anomaly = []

    Q_aphelion_dist = []

    n_motion = []

    T_orbital_period = []

    TisserandJ = []

    # looping through each month in the year
    for month in month_list:

        # Analyse recorded meteor data monthly 
        traj_file_content = dd.get_monthly_file_content_by_date(month)

        # Read data as a Pandas DataFrame
        traj_df = meteor_trajectory_reader.read_data(traj_file_content)
        
        for ix in range(len(traj_df['a (AU)'])):
            
            identity = traj_df.index[ix]

            a = traj_df['a (AU)'][ix]
            sigma_a = traj_df['+/- (sigma.9)'][ix]

            e = traj_df['e'][ix]
            sigma_e = traj_df['+/- (sigma.10)'][ix]

            i = traj_df['i (deg)'][ix]
            sigma_i = traj_df['+/- (sigma.11)'][ix]

            peri = traj_df['peri (deg)'][ix]
            sigma_peri = traj_df['+/- (sigma.12)'][ix]

            node = traj_df['node (deg)'][ix]
            sigma_node = traj_df['+/- (sigma.13)'][ix]

            Pi = traj_df['Pi (deg)'][ix]

            b = traj_df['b (deg)'][ix]

            q = traj_df['q (AU)'][ix]

            f = traj_df['f (deg)'][ix]

            M = traj_df['M (deg)'][ix]

            Q = traj_df['Q (AU)'][ix]

            n = traj_df['n (deg/day)'][ix]

            T = traj_df['T (years)'][ix]

            TisandJ = traj_df['TisserandJ'][ix]

            arb = [-10000, 9999] # arb as in arbitrary

            if check_conditions(a, 1.126391025894812 - 0.2, 1.126391025894812 + 0.2,
                                e, 0.2037450762416414 - 0.2, 0.2037450762416414 + 0.2,
                                i, 6.03494377024794 - 10, 6.03494377024794 + 10,
                                peri, 66.22306084084298 - 10, 66.22306084084298 + 10,
                                node, 2.06086619569642 - 10, 2.06086619569642 + 10,
                                Pi, arb[0], arb[1],
                                b, arb[0], arb[1],
                                q, arb[0], arb[1],
                                f, arb[0], arb[1],
                                M, arb[0], arb[1],
                                Q, arb[0], arb[1],
                                n, arb[0], arb[1],
                                T, arb[0], arb[1],
                                TisandJ, arb[0], arb[1]):
                
                identifiers.append(identity)

                a_semi_major_axis.append(a)
                sigma_a_semi_major_axis.append(sigma_a)

                eccentricity.append(e)
                sigma_eccentricity.append(sigma_e)

                inclination.append(i)
                sigma_inclination.append(sigma_i)

                peri_argument.append(peri) 
                sigma_peri_argument.append(sigma_peri)

                ascending_node.append(node) 
                sigma_ascending_node.append(sigma_node)

                Pi_peri_longitude.append(Pi) 

                b_peri_latitude.append(b) 

                q_peri_distance.append(q) 

                f_true_anomaly.append(f) 

                M_mean_anomaly.append(M) 

                Q_aphelion_dist.append(Q) 

                n_motion.append(n) 

                T_orbital_period.append(T) 

                TisserandJ.append(TisandJ)
                '''
                print('identity :', identity)
                print('a =', a)
                print('sigma a = ', sigma_a)
                print('e =', e)
                print('sigma e = ', sigma_e)
                print('i =', i)
                print('sigma i = ', sigma_i)
                print('peri =', peri)
                print('sigma peri = ', sigma_peri)
                print('node =', node)
                print('sigma node = ', sigma_node)
                print()
                '''

                obj = Meteor(e, q, i, node, peri)
                print("asteroid obj created")
                asteroid_obj_list.append(obj)

    # add year to system lists
    system_identifiers += identifiers

    system_a_semi_major_axis += a_semi_major_axis
    system_sigma_a_semi_major_axis += sigma_a_semi_major_axis

    system_e_eccentricity += eccentricity
    system_sigma_eccentricity += sigma_eccentricity

    system_i_inclination += inclination
    system_sigma_inclination += sigma_inclination

    system_peri_argument += peri_argument
    system_sigma_peri_argument += sigma_peri_argument

    system_ascending_node += ascending_node
    system_sigma_ascending_node += sigma_ascending_node

    system_Pi_peri_longitude += Pi_peri_longitude

    system_b_peri_latitude += b_peri_latitude

    system_q_peri_distance += q_peri_distance

    system_f_true_anomaly += f_true_anomaly

    system_M_mean_anomaly += M_mean_anomaly

    system_Q_aphelion_dist += Q_aphelion_dist

    system_n_motion += n_motion

    system_T_orbital_period += T_orbital_period

    system_TisserandJ += TisserandJ
