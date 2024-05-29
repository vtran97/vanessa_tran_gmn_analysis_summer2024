'''
GMN datamining 

Vanessa Tran (vtran97@uwo.ca)
May 1st to August 16 (2024)

This file searches through the entire GMN database and searches through orbital elements using
min and max values
- used primarily for Bennu searches (2024-05-29)
- asteroid function a child class of Orbit class from sbpy
    - the function D_Criterion is edited; to work with GMN data, it has been changed to work 
      with self and obj instead of with two bodies given through the from_horizons function of 
      the Orbit class from sbpy
    - the order of self nad obj DOES NOT matter -- it will give you the same value no matter 
      which way you decide to type your self/obj order
    - 
'''

# -----------------------------------------------------------------------------------------------------------
# imports - DO NOT DELETE!!!

# GMN
from gmn_python_api import data_directory as dd
from gmn_python_api import meteor_trajectory_reader

# get all months
from get_all_months import get_all_months_by_year_list

# for D values
from d_value_meteor_class import Meteor

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
    '''checks for all orbital elements conditions -- optimize!!'''

    conditions_list = []

    if a > a_min and a < a_max :
        conditions_list.append(True)

    if e > e_min and e < e_max:
        conditions_list.append(True)
    
    if i > i_min and i < i_max and i_min > 0 and i_max < 360:
        conditions_list.append(True)
    elif i_min < 0:
        # editing the restrictions since i angle covers interval before and after zero degrees
        # angle wrapping can be done for all of the other elements as well -- follow template below
        i_sub_min = 360 + i_min
        i_sub_max = 360
        # reset i min to 0 for interval 
        i_min = 0
        if i > i_min and i < i_max or i < i_sub_max and i > i_sub_min:
            conditions_list.append(True)
    elif i_max > 360:
        i_sub_min = 0
        i_sub_max = i_max - 360
        i_max = 360
        if i > i_min and i < i_max or i < i_sub_max and i > i_sub_min:
            conditions_list.append(True)

    if peri > peri_min and peri < peri_max and peri_min > 0 and peri_max < 360:
        conditions_list.append(True)
    elif peri_min < 0:
        peri_sub_min = 360 + peri_min
        peri_sub_max = 360
        peri_min = 0
        if peri > peri_min and peri < peri_max or peri < peri_sub_max and peri > peri_sub_min:
            conditions_list.append(True)
    elif peri_max > 360:
        peri_sub_min = 0
        peri_sub_max = i_max - 360
        peri_max = 360
        if peri > peri_min and peri < peri_max or peri < peri_sub_max and peri > peri_sub_min:
            conditions_list.append(True)

    if node > node_min and node < node_max and node_min > 0 and node_max < 360:
        conditions_list.append(True)
    elif node_min < 0:
        node_sub_min = 360 + node_min
        node_sub_max = 360
        node_min = 0
        if node > node_min and node < node_max or node < node_sub_max and node > node_sub_min:
            conditions_list.append(True)
    elif node_max > 360:
        node_sub_min = 0
        node_sub_max = i_max - 360
        node_max = 360
        if node > node_min and node < node_max or node < node_sub_max and node > node_sub_min:
            conditions_list.append(True)
  
    if Pi > Pi_min and Pi < Pi_max:
        conditions_list.append(True)
    if b > b_min and b < b_max:
        conditions_list.append(True)
    if q > q_min and q < q_max:
        conditions_list.append(True)
    if f > f_min and f < f_max:
        conditions_list.append(True)
    if M > M_min and M < M_max:
        conditions_list.append(True)
    if Q > Q_min and Q < Q_max:
        conditions_list.append(True)
    if n > n_min and n < n_max:
        conditions_list.append(True)
    if T > T_min and T < T_max:
        conditions_list.append(True)
    if TisserandJ > TisserandJ_min and TisserandJ < TisserandJ_max:
        conditions_list.append(True)

    if len(conditions_list) == 14:
        return True
    else:
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

bennu_asteroid_obj_list = []

# arb as in arbitrary -- used for any non specific calculations for criteria for conditions later
arb = [-10000, 9999] 

# looping through all year data
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
            # get all information needde from the dataframe
            
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

            # BENNU --------------------------------------------------------------------

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

                # create asteroid object and append to list to check against Bennu later
                obj = Meteor(identity, e, q, i, node, peri)
                print("asteroid obj created")
                bennu_asteroid_obj_list.append(obj)

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

# -----------------------------------------------------------------------------------------------------------
# BENNU
# check for d values --> use the D criterion

# Asteroid(e, q, i, omega [NODE], w [PERI])
bennu_ephemeris = Meteor('Bennu', .2037450762416414, .8968944004459729, 6.03494377024794, 2.06086619569642, 66.22306084084298) 
# bennu info taken from Horizons Web Application - 101955 Bennu (1999 RQ36)

bennu_from_horizon_updated = Meteor('Bennu', 0.2037482514536186, 0.89654206, 6.03301417, 1.98511762, 66.37138491)
# bennu info taken from the from_horizons method and printed -- these are likely updated? 

# try bennu against all other potential asteroids
for meteor_obj in bennu_asteroid_obj_list:

    # Southworth & Hawkins function
    D_SH_e = bennu_ephemeris.D_criterion(meteor_obj)
    # Drummond function
    D_D_e = bennu_ephemeris.D_criterion(meteor_obj, version='d')

    # Southworth & Hawkins function
    D_SH_fhu = bennu_from_horizon_updated.D_criterion(meteor_obj)
    # Drummond function
    D_D_fhu = bennu_from_horizon_updated.D_criterion(meteor_obj, version='d')

    print("\n-------------")
    print(meteor_obj.identity)

    print("\nFROM HORIZONS (LATEST EPOCH)")
    print('D_SH', D_SH_fhu)
    print('D_D', D_D_fhu)

    print("\nEPHEMERIS - WEB APP")
    print('D_SH', D_SH_e)
    print('D_D', D_D_e)

    print("\nDifference")
    print("D_SH", abs(D_SH_e - D_SH_fhu))
    print("D_D", abs(D_D_e - D_D_fhu))
    print("-------------")

