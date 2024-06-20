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

# graph
import matplotlib.pyplot as plt
import pandas as pd

# get all months
from functions import get_all_months_by_year_list, check_conditions_orbital, narrow_dataframe_orbital_5d

# for D values
from d_value_meteor_class import Meteor

# math
import math

# -----------------------------------------------------------------------------------------------------------
# dataminings starts here
# -----------------------------------------------------------------------------------------------------------

# data for all months
all_months = get_all_months_by_year_list()

def get_number_per_unit_volume(mods, cond):
# if we're looking for multiple asteroid types, can create multiple lists :)

  asteroid_list = []
  #asteroid_obj_list = []

  #year = month_list[0].split("-")[0]

  # print(f"\n************\nYEAR : {year}\n************")

  # lists to be reset for each year
  identifiers = []

  a_semi_major_axis = []
  #sigma_a_semi_major_axis = []

  eccentricity = []
  #sigma_eccentricity = []

  inclination = []
  #sigma_inclination = []

  peri_argument = []
  #sigma_peri_argument = []

  ascending_node = []
  #sigma_ascending_node = []

  vgeo = []

  rageo = []

  decgeo = []

  # nonconditional

  q_peri_distance = []

  '''Pi_peri_longitude = []

  b_peri_latitude = []

  f_true_anomaly = []

  M_mean_anomaly = []

  Q_aphelion_dist = []

  n_motion = []

  T_orbital_period = []

  TisserandJ = []'''

  # other parameters

  '''duration = []

  peak_absolute_mag = []

  peak_height = []

  F_param = []

  mass_tau = []

  Qc = []'''

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
              #sigma_a = traj_df['+/- (sigma.8)'][ix]

              e = traj_df['e'][ix]
              #sigma_e = traj_df['+/- (sigma.9)'][ix]

              i = traj_df['i (deg)'][ix]
              #sigma_i = traj_df['+/- (sigma.10)'][ix]

              peri = traj_df['peri (deg)'][ix]
              #sigma_peri = traj_df['+/- (sigma.11)'][ix]

              node = traj_df['node (deg)'][ix]
              #sigma_node = traj_df['+/- (sigma.12)'][ix]
              '''
              Pi = traj_df['Pi (deg)'][ix]

              b = traj_df['b (deg)'][ix]
              '''
              q = traj_df['q (AU)'][ix]
              '''
              f = traj_df['f (deg)'][ix]

              M = traj_df['M (deg)'][ix]

              Q = traj_df['Q (AU)'][ix]

              n = traj_df['n (deg/day)'][ix]

              T = traj_df['T (years)'][ix]

              TisandJ = traj_df['TisserandJ'][ix]

              dur = traj_df['Duration (sec)'][ix]

              peak_abs_mag = traj_df['Peak (AbsMag)'][ix]

              peak_ht = traj_df['Peak Ht (km)'][ix]

              F = traj_df['F (param)'][ix]

              mass = traj_df['Mass kg (tau=0.7%)'][ix]

              qc = traj_df['Qc (deg)'][ix]'''

              RAgeo = traj_df['RAgeo (deg)'][ix]

              Decgeo = traj_df['DECgeo (deg)'][ix]

              Vgeo = traj_df['Vgeo (km/s)'][ix]


              # BENNU --------------------------------------------------------------------

              '''
              for conditions, put the actual value and then add/subtract inside of the arguments. 
              the code is designed to wrap around any angles as long as the angles are out of bounds. 
              no need to convert degrees to their backrotation / forward rotation. 
              see below for example of range ---> i min 
              '''
              
              if check_conditions_orbital(a, cond[0], cond[1]-mods[0], cond[1]+mods[0],
                                          e, cond[2], cond[3]-mods[0], cond[3]+mods[0],
                                          i, cond[4], cond[5]-mods[1], cond[5]+mods[1],
                                          peri, cond[6], cond[7]-mods[1], cond[7]+mods[1],
                                          node, cond[8], cond[9]-mods[1], cond[9]+mods[1]) == True:
                  
                  # orb elems

                  #print("----------------------")

                  identifiers.append(identity)
                  #print('identity', identity)

                  a_semi_major_axis.append(a)
                  #print('a', a)
                  #sigma_a_semi_major_axis.append(sigma_a)

                  eccentricity.append(e)
                  #print('e', e)
                  #sigma_eccentricity.append(sigma_e)

                  inclination.append(i)
                  #print('i', i)
                  #sigma_inclination.append(sigma_i)

                  peri_argument.append(peri) 
                  #print('peri', peri)
                  #sigma_peri_argument.append(sigma_peri)

                  ascending_node.append(node) 
                  #print('node', node)
                  #sigma_ascending_node.append(sigma_node)

                  vgeo.append(Vgeo)

                  rageo.append(RAgeo)

                  decgeo.append(Decgeo)

                  '''# nonconditional

                  Pi_peri_longitude.append(Pi) 

                  b_peri_latitude.append(b) 
                  '''
                  q_peri_distance.append(q) 
                  '''
                  f_true_anomaly.append(f) 

                  M_mean_anomaly.append(M) 

                  Q_aphelion_dist.append(Q) 

                  n_motion.append(n) 

                  T_orbital_period.append(T) 

                  TisserandJ.append(TisandJ)

                  # others

                  duration.append(dur)

                  peak_absolute_mag.append(peak_abs_mag)

                  peak_height.append(peak_ht)

                  F_param.append(F)

                  mass_tau.append(mass)

                  Qc.append(qc)'''

                  # create asteroid object and append to list to check against Bennu later

                  obj = Meteor(identity, e, q, i, node, peri)
                  # print("asteroid obj created")
                  asteroid_list.append(obj)
              
      # add year to system lists
      '''
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
      '''
      # -----------------------------------------------------------------------------------------------------------
      # BENNU
      # check for d values --> use the D criterion
      '''
      # Asteroid(e, q, i, omega [NODE], w [PERI])
      bennu_ephemeris = Meteor('Bennu', 0.2037450762416414, 0.8968944004459729, 6.03494377024794, 2.06086619569642, 66.22306084084298) 
      # bennu info taken from Horizons Web Application - 101955 Bennu (1999 RQ36)
      # for extra info : https://ssd.jpl.nasa.gov/horizons/manual.html#search

      bennu_from_horizon_updated = Meteor('Bennu', 0.2037482514536186, 0.89654206, 6.03301417, 1.98511762, 66.37138491)
      # bennu info taken from the from_horizons method and printed -- these are likely updated? 

      index = 0

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

        print("\nSD Error")
        print("a =", system_sigma_a_semi_major_axis[index])
        print("e =", system_sigma_eccentricity[index])
        print("i =", system_sigma_inclination[index])
        print("node =", system_sigma_ascending_node[index])
        print("peri =", system_sigma_peri_argument[index])
        print()
        print("Duration (sec_ :", system_duration[index])
        print("Peak (Abs Mag) :", system_peak_abs_mag[index])
        print("Peak height (km) :", system_peak_height[index])
        print("F (param) :", system_F_param[index])
        print("Mass (kg), tau = 0.7% :", system_mass_tau[index])
        print("Qc (deg) :", system_Qc[index])

        print("\nFROM HORIZONS (LATEST EPOCH) - 2460460.2864766")
        print('D_SH', D_SH_fhu)
        print('D_D', D_D_fhu)

        print("\nEPHEMERIS - WEB APP - 2455562.5")
        print('D_SH', D_SH_e)
        print('D_D', D_D_e)

        print("\nDifference")
        print("D_SH", abs(D_SH_e - D_SH_fhu))
        print("D_D", abs(D_D_e - D_D_fhu))
        print("-------------")

        index += 1
        '''

      # check aei space -------------------------------------------
      '''
      Consider a "volume" of orbital element space. For example, consider the semimajor axis a, 
      eccentricity e and inclination i as three dimensions. You've selected all the candidates in a 
      certain range of a,e and i. You could define a number per unit volume by dividing the number 
      of meteors GMN has in that volume by the volume of this aei space. Now imagine making this 
      volume bigger and bigger by taking larger ranges of a, e and i. If there is a concentration 
      near the asteroid's aei, then the number of meteors per unit volume should drop gradually to the 
      background level as you increase your sampling volume.
      '''
  d = {'candidates' : tuple(identifiers), 
       'semi major axis (a)' : tuple(a_semi_major_axis), 
       'eccentricity (e)' : tuple(eccentricity), 
       'inclination (i)' : tuple(inclination), 
       'perihelion arugment (peri)' : tuple(peri_argument), 
       'ascending node (node)' : tuple(ascending_node)}
  df = pd.DataFrame(d)
  
  '''print("'df within function'")
  print(df)'''

  number_candidates = len(identifiers)
  volume = (mods[0]*2) ** 2 * (mods[1]*2) ** 3

  number_per_unit_volume = number_candidates / volume

  #print('\nidentifiers:', identifiers)

  print('candidates         :', number_candidates)
  print('volume             :', volume)
  print('number/unit volume :', number_per_unit_volume)

  unit_per_volume_list.append(number_per_unit_volume)
  volume_list.append(volume)

  return df,asteroid_list

# run values for graphs ------------------------------------------

# bennu conditions for 5d space, a e i peri node

conds_bennu = [True, 1.126391025894812, 
              True, 0.2037450762416414,
              True, 6.03494377024794, 
              True, 66.22306084084298,
              True, 2.06086619569642]

# swift tuttle conds for 5d space
conds_swift_tuttle = [True, 26.0920694978266, 
                      True, 0.963225755046038,
                      True, 113.453816997171, 
                      True, 152.9821676305871,
                      True, 139.3811920815948]

conds_eros = [True, 1.458177646485403, 
              True, 0.2227072743779392, 
              True, 10.82762857430502, 
              True, 178.8953167089443, 
              True, 304.2765731967428]

conds_itokawa = [True, 1.324142578587497,
                 True, 0.2803311777299725,
                 True, 1.621207668814055,
                 True, 162.8211329499564, 
                 True, 69.0761042651376]

conds_toutatis = [True, 2.543728029076248, 
                  True, 0.624758896480083, 
                  True, 0.4480680353844077, 
                  True, 277.868771555242, 
                  True, 125.3549352905831]

conds_ryugu = [True, 1.191013624852465, 
               True, 0.1910659421644889,
               True, 5.866516749812472,
               True, 211.6156610065788,
               True, 251.2954193296629]

conds_didymos = [True, 1.64268149873718,
                 True, 0.3832302498647931,
                 True, 3.414222573974985,
                 True, 319.5916377730013,
                 True, 72.9867658813169]

# swift tuttle -- good interval ------------------------------
'''
print("\n-----------------------------------------------------------\nSWIFT-TUTTLE")

unit_per_volume_list = []
volume_list = []

# make the largest interval and then narrow from there!
modifiers_5d = [0.2,
                20]

dataframe = get_number_per_unit_volume(modifiers_5d, conds_swift_tuttle)

for idx in range(35):

    ndo5d = narrow_dataframe_orbital_5d(dataframe, modifiers_5d, conds_swift_tuttle)
    units_per_vol = len(ndo5d[1]) / ndo5d[0]
    volume = ndo5d[0]

    unit_per_volume_list.append(units_per_vol)
    volume_list.append(volume)

    print()
    print("modifiers    :", modifiers_5d)
    print('# candidates :', len(ndo5d[1]))
    print('volume       :', volume)
    print('# / v        :', units_per_vol)

    if idx >= 30:
        print('candidate list:', ndo5d[1])

    modifiers_5d[0] -= 0.005 
    modifiers_5d[1] -=  0.5

vol_list_log = []
upv_list_log = []

for j in range(len(volume_list)):
  try:
    log_vol = math.log(volume_list[j])
    log_npv = math.log(unit_per_volume_list[j])
    upv_list_log.append(log_npv)
    vol_list_log.append(log_vol)
  except ValueError as e:
    print("math domain error, npuv is negative or = 0")

graph = plt.plot(vol_list_log, upv_list_log)
plt.xlabel("volume (ln)")
plt.ylabel("number per unit volume (ln)")
plt.title("npuv 5d : swift-tuttle")
plt.grid()
plt.show()
'''
# bennu -- good interval ------------------------------------------------------------------------------------------------------

# Asteroid(e, q, i, omega [NODE], w [PERI])
bennu_ephemeris = Meteor('Bennu', 0.2037450762416414, 0.8968944004459729, 6.03494377024794, 2.06086619569642, 66.22306084084298) 
bennu_from_horizon_updated = Meteor('Bennu', 0.2037482514536186, 0.89654206, 6.03301417, 1.98511762, 66.37138491)

index = 0

print("\n-----------------------------------------------------------")
print("BENNU")

unit_per_volume_list = []
volume_list = []

# make the largest interval and then narrow from there!
modifiers_5d = [0.2,
                20]

get_npuv = get_number_per_unit_volume(modifiers_5d, conds_bennu)
dataframe = get_npuv[0]

for idx in range(20):

    ndo5d = narrow_dataframe_orbital_5d(dataframe, modifiers_5d, conds_bennu)
    units_per_vol = len(ndo5d[1]) / ndo5d[0]
    volume = ndo5d[0]

    unit_per_volume_list.append(units_per_vol)
    volume_list.append(volume)

    print()
    print("modifiers    :", modifiers_5d)
    print('# candidates :', len(ndo5d[1]))
    print('volume       :', volume)
    print('# / v        :', units_per_vol)

    print('candidate list:', ndo5d[1])

    modifiers_5d[0] -= 0.005 
    modifiers_5d[1] -=  0.5

# print(asteroid_list)

# try bennu against all other potential asteroids
for meteor_obj in get_npuv[1]:

  # Southworth & Hawkins function
  D_SH_e = bennu_ephemeris.D_criterion(meteor_obj)
  # Drummond function
  D_D_e = bennu_ephemeris.D_criterion(meteor_obj, version='d')
  # hybrid
  D_HYB_e = bennu_ephemeris.D_criterion(meteor_obj, version='h')

  # Southworth & Hawkins function
  D_SH_fhu = bennu_from_horizon_updated.D_criterion(meteor_obj)
  # Drummond function
  D_D_fhu = bennu_from_horizon_updated.D_criterion(meteor_obj, version='d')
  # hybrid
  D_HYB_fhu = bennu_ephemeris.D_criterion(meteor_obj, version='h')

  print("\n-------------")
  meteor_obj.get_attr()

  print("\nFROM HORIZONS (LATEST EPOCH) - 2460460.2864766")
  print('D_SH', D_SH_fhu)
  print('D_D', D_D_fhu)
  print('D HYBRID', D_HYB_e)

  print("\nEPHEMERIS - WEB APP - 2455562.5")
  print('D_SH', D_SH_e)
  print('D_D', D_D_e)
  print('D HYBRID', D_HYB_fhu)

  print("\nDifference")
  print("D_SH", abs(D_SH_e - D_SH_fhu))
  print("D_D", abs(D_D_e - D_D_fhu))
  print("-------------")

  index += 1

graph = plt.plot(volume_list, unit_per_volume_list)
plt.xlabel("volume")
plt.ylabel("number per unit volume")
plt.title("npuv 5d : bennu")
plt.grid()
plt.show()

vol_list_log = []
upv_list_log = []

for j in range(len(volume_list)):
  try:
    log_vol = math.log(volume_list[j])
    log_npv = math.log(unit_per_volume_list[j])
    upv_list_log.append(log_npv)
    vol_list_log.append(log_vol)
  except ValueError as e:
    print("math domain error, npuv is negative or = 0")

graph = plt.plot(vol_list_log, upv_list_log)
plt.xlabel("volume (ln)")
plt.ylabel("number per unit volume (ln)")
plt.title("npuv 5d : bennu (ln)")
plt.grid()
plt.show()

# 433 eros -- good interval ------------------------------------------------------------------------------------------------------
'''
# Asteroid(e, q, i, omega [NODE], w [PERI])
eros = Meteor('Eros', 0.2227072743779392, 1.133430877277801, 10.82762857430502, 304.2765731967428, 178.8953167089443)

index = 0

print("\n-----------------------------------------------------------")
print("EROS")

unit_per_volume_list = []
volume_list = []

# make the largest interval and then narrow from there!
modifiers_5d = [0.2,
                20]

get_npuv = get_number_per_unit_volume(modifiers_5d, conds_eros)
dataframe = get_npuv[0]

for idx in range(30):

    ndo5d = narrow_dataframe_orbital_5d(dataframe, modifiers_5d, conds_eros)
    units_per_vol = len(ndo5d[1]) / ndo5d[0]
    volume = ndo5d[0]

    unit_per_volume_list.append(units_per_vol)
    volume_list.append(volume)

    print()
    print("modifiers    :", modifiers_5d)
    print('# candidates :', len(ndo5d[1]))
    print('volume       :', volume)
    print('# / v        :', units_per_vol)

    print('candidate list:', ndo5d[1])

    modifiers_5d[0] -= 0.005 
    modifiers_5d[1] -=  0.5

# print(get_npuv[1])

# try eros against all other potential asteroids
for meteor_obj in get_npuv[1]:

  # Southworth & Hawkins function
  D_SH = eros.D_criterion(meteor_obj)
  # Drummond function
  D_D = eros.D_criterion(meteor_obj, version='d')

  print("\n-------------")
  meteor_obj.get_attr()

  print("\nD VALS")
  print('D_SH', D_SH)
  print('D_D', D_D)

  index += 1

graph = plt.plot(volume_list, unit_per_volume_list)
plt.xlabel("volume")
plt.ylabel("number per unit volume")
plt.title("npuv 5d : eros")
plt.grid()
plt.show()

vol_list_log = []
upv_list_log = []

for j in range(len(volume_list)):
  try:
    log_vol = math.log(volume_list[j])
    log_npv = math.log(unit_per_volume_list[j])
    upv_list_log.append(log_npv)
    vol_list_log.append(log_vol)
  except ValueError as e:
    print("math domain error, npuv is negative or = 0")

graph = plt.plot(vol_list_log, upv_list_log)
plt.xlabel("volume (ln)")
plt.ylabel("number per unit volume (ln)")
plt.title("npuv 5d : eros (ln)")
plt.grid()
plt.show()
'''
# Itokawa -- good interval ------------------------------------------------------------------------------------------------------
'''
# Asteroid(e, q, i, omega [NODE], w [PERI])
itokawa = Meteor('Itokawa', 0.2803311777299725, 0.9529441300496611, 1.621207668814055, 69.0761042651376, 162.8211329499564)

index = 0

print("\n-----------------------------------------------------------")
print("ITOKAWA")

unit_per_volume_list = []
volume_list = []

# make the largest interval and then narrow from there!
modifiers_5d = [0.2,
                20]

get_npuv = get_number_per_unit_volume(modifiers_5d, conds_itokawa)
dataframe = get_npuv[0]

for idx in range(30):

    ndo5d = narrow_dataframe_orbital_5d(dataframe, modifiers_5d, conds_itokawa)
    units_per_vol = len(ndo5d[1]) / ndo5d[0]
    volume = ndo5d[0]

    unit_per_volume_list.append(units_per_vol)
    volume_list.append(volume)

    print()
    print("modifiers    :", modifiers_5d)
    print('# candidates :', len(ndo5d[1]))
    print('volume       :', volume)
    print('# / v        :', units_per_vol)

    print('candidate list:', ndo5d[1])

    modifiers_5d[0] -= 0.005 
    modifiers_5d[1] -=  0.5

# print(get_npuv[1])

# try itokawa against all other potential asteroids
for meteor_obj in get_npuv[1]:

  # Southworth & Hawkins function
  D_SH = itokawa.D_criterion(meteor_obj)
  # Drummond function
  D_D = itokawa.D_criterion(meteor_obj, version='d')

  print("\n-------------")
  meteor_obj.get_attr()

  print("\nD VALS")
  print('D_SH', D_SH)
  print('D_D', D_D)

  index += 1

graph = plt.plot(volume_list, unit_per_volume_list)
plt.xlabel("volume")
plt.ylabel("number per unit volume")
plt.title("npuv 5d : itokawa")
plt.grid()
plt.show()

vol_list_log = []
upv_list_log = []

for j in range(len(volume_list)):
  try:
    log_vol = math.log(volume_list[j])
    log_npv = math.log(unit_per_volume_list[j])
    upv_list_log.append(log_npv)
    vol_list_log.append(log_vol)
  except ValueError as e:
    print("math domain error, npuv is negative or = 0")

graph = plt.plot(vol_list_log, upv_list_log)
plt.xlabel("volume (ln)")
plt.ylabel("number per unit volume (ln)")
plt.title("npuv 5d : itokawa (ln)")
plt.grid()
plt.show()
'''
# Toutatis -- good interval ------------------------------------------------------------------------------------------------------
'''
# Asteroid(e, q, i, omega [NODE], w [PERI])
toutatis = Meteor('Toutatis', 0.624758896480083, 0.9545113126851149, 0.4480680353844077, 125.3549352905831, 277.868771555242)

index = 0

print("\n-----------------------------------------------------------")
print("TOUTATIS")

unit_per_volume_list = []
volume_list = []

# make the largest interval and then narrow from there!
modifiers_5d = [0.2,
                20]

get_npuv = get_number_per_unit_volume(modifiers_5d, conds_toutatis)
dataframe = get_npuv[0]

for idx in range(20):

    ndo5d = narrow_dataframe_orbital_5d(dataframe, modifiers_5d, conds_toutatis)
    units_per_vol = len(ndo5d[1]) / ndo5d[0]
    volume = ndo5d[0]

    unit_per_volume_list.append(units_per_vol)
    volume_list.append(volume)

    print()
    print("modifiers    :", modifiers_5d)
    print('# candidates :', len(ndo5d[1]))
    print('volume       :', volume)
    print('# / v        :', units_per_vol)

    print('candidate list:', ndo5d[1])

    modifiers_5d[0] -= 0.005 
    modifiers_5d[1] -=  0.5

# print(get_npuv[1])

# try toutatis against all other potential asteroids
for meteor_obj in get_npuv[1]:

  # Southworth & Hawkins function
  D_SH = toutatis.D_criterion(meteor_obj)
  # Drummond function
  D_D = toutatis.D_criterion(meteor_obj, version='d')

  print("\n-------------")
  meteor_obj.get_attr()

  print("\nD VALS")
  print('D_SH', D_SH)
  print('D_D', D_D)

  index += 1

graph = plt.plot(volume_list, unit_per_volume_list)
plt.xlabel("volume")
plt.ylabel("number per unit volume")
plt.title("npuv 5d : toutatis")
plt.grid()
plt.show()

vol_list_log = []
upv_list_log = []

for j in range(len(volume_list)):
  try:
    log_vol = math.log(volume_list[j])
    log_npv = math.log(unit_per_volume_list[j])
    upv_list_log.append(log_npv)
    vol_list_log.append(log_vol)
  except ValueError as e:
    print("math domain error, npuv is negative or = 0")

graph = plt.plot(vol_list_log, upv_list_log)
plt.xlabel("volume (ln)")
plt.ylabel("number per unit volume (ln)")
plt.title("npuv 5d : toutatis (ln)")
plt.grid()
plt.show()
'''
# Ryugu -- good interval ------------------------------------------------------------------------------------------------------
'''
# Asteroid(e, q, i, omega [NODE], w [PERI])
ryugu = Meteor('Ryugu', 0.1910659421644889, 0.963451484489286, 5.866516749812472, 251.2954193296629, 211.6156610065788)

index = 0

print("\n-----------------------------------------------------------")
print("RYUGU")

unit_per_volume_list = []
volume_list = []

# make the largest interval and then narrow from there!
modifiers_5d = [0.2,
                20]

get_npuv = get_number_per_unit_volume(modifiers_5d, conds_ryugu)
dataframe = get_npuv[0]

for idx in range(20):

    ndo5d = narrow_dataframe_orbital_5d(dataframe, modifiers_5d, conds_ryugu)
    units_per_vol = len(ndo5d[1]) / ndo5d[0]
    volume = ndo5d[0]

    unit_per_volume_list.append(units_per_vol)
    volume_list.append(volume)

    print()
    print("modifiers    :", modifiers_5d)
    print('# candidates :', len(ndo5d[1]))
    print('volume       :', volume)
    print('# / v        :', units_per_vol)

    print('candidate list:', ndo5d[1])

    modifiers_5d[0] -= 0.005 
    modifiers_5d[1] -=  0.5

print(get_npuv[1])

# try ryugu against all other potential asteroids
for meteor_obj in get_npuv[1]:

  # Southworth & Hawkins function
  D_SH = ryugu.D_criterion(meteor_obj)
  # Drummond function
  D_D = ryugu.D_criterion(meteor_obj, version='d')

  print("\n-------------")
  meteor_obj.get_attr()

  print("\nD VALS")
  print('D_SH', D_SH)
  print('D_D', D_D)

  index += 1

graph = plt.plot(volume_list, unit_per_volume_list)
plt.xlabel("volume")
plt.ylabel("number per unit volume")
plt.title("npuv 5d : ryugu")
plt.grid()
plt.show()

vol_list_log = []
upv_list_log = []

for j in range(len(volume_list)):
  try:
    log_vol = math.log(volume_list[j])
    log_npv = math.log(unit_per_volume_list[j])
    upv_list_log.append(log_npv)
    vol_list_log.append(log_vol)
  except ValueError as e:
    print("math domain error, npuv is negative or = 0")

graph = plt.plot(vol_list_log, upv_list_log)
plt.xlabel("volume (ln)")
plt.ylabel("number per unit volume (ln)")
plt.title("npuv 5d : ryugu (ln)")
plt.grid()
plt.show()
'''
# Didymos -- good interval ------------------------------------------------------------------------------------------------------

# Asteroid(e, q, i, omega [NODE], w [PERI])
didymos = Meteor('Didymos', 0.3832302498647931, 1.013156257527858, 3.414222573974985, 72.9867658813169, 319.5916377730013)

index = 0

print("\n-----------------------------------------------------------")
print("DIDYMOS")

unit_per_volume_list = []
volume_list = []

# make the largest interval and then narrow from there!
modifiers_5d = [0.2,
                20]

get_npuv = get_number_per_unit_volume(modifiers_5d, conds_didymos)
dataframe = get_npuv[0]

for idx in range(20):

    ndo5d = narrow_dataframe_orbital_5d(dataframe, modifiers_5d, conds_didymos)
    units_per_vol = len(ndo5d[1]) / ndo5d[0]
    volume = ndo5d[0]

    unit_per_volume_list.append(units_per_vol)
    volume_list.append(volume)

    print()
    print("modifiers    :", modifiers_5d)
    print('# candidates :', len(ndo5d[1]))
    print('volume       :', volume)
    print('# / v        :', units_per_vol)

    print('candidate list:', ndo5d[1])

    modifiers_5d[0] -= 0.005 
    modifiers_5d[1] -=  0.5

print(get_npuv[1])

# try didymos against all other potential asteroids
for meteor_obj in get_npuv[1]:

  # Southworth & Hawkins function
  D_SH = didymos.D_criterion(meteor_obj)
  # Drummond function
  D_D = didymos.D_criterion(meteor_obj, version='d')

  print("\n-------------")
  meteor_obj.get_attr()

  print("\nD VALS")
  print('D_SH', D_SH)
  print('D_D', D_D)

  index += 1

graph = plt.plot(volume_list, unit_per_volume_list)
plt.xlabel("volume")
plt.ylabel("number per unit volume")
plt.title("npuv 5d : didymos")
plt.grid()
plt.show()

vol_list_log = []
upv_list_log = []

for j in range(len(volume_list)):
  try:
    log_vol = math.log(volume_list[j])
    log_npv = math.log(unit_per_volume_list[j])
    upv_list_log.append(log_npv)
    vol_list_log.append(log_vol)
  except ValueError as e:
    print("math domain error, npuv is negative or = 0")

graph = plt.plot(vol_list_log, upv_list_log)
plt.xlabel("volume (ln)")
plt.ylabel("number per unit volume (ln)")
plt.title("npuv 5d : didymos (ln)")
plt.grid()
plt.show()