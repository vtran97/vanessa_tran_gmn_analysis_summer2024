'''
Reduced Asteorids for Orbital Elements 

Vanessa Tran (vtran97@uwo.ca)
May 1st to August 16 (2024)

Main question : Does the reduction of slower meteors change the orbital elements a lot, 
or are we able to just pull the data as it comes out from the GMN? 
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

#------------------------------------------------------------------------------------------------------------

# Asteroid(e, q, i, omega [NODE], w [PERI])
bennu_ephemeris = Meteor('Bennu', 0.2037450762416414, 0.8968944004459729, 6.03494377024794, 2.06086619569642, 66.22306084084298) 
bennu_from_horizon_updated = Meteor('Bennu', 0.2037482514536186, 0.89654206, 6.03301417, 1.98511762, 66.37138491)
itokawa = Meteor('Itokawa', 0.2803311777299725, 0.9529441300496611, 1.621207668814055, 69.0761042651376, 162.8211329499564)

old = Meteor('old', 0.259309, 1.010822, 1.973017, 71.348268, 169.633876)
new = Meteor('new', 0.259563,  1.010817, 1.978857, 71.347847, 169.629973)

# OLD 

print("OLD")

# Southworth & Hawkins function
D_SH = itokawa.D_criterion(old)
# Drummond function
D_D = itokawa.D_criterion(old, version='d')

print('D_SH', D_SH)
print('D_D', D_D)

'''# Southworth & Hawkins function
D_SH_e = bennu_ephemeris.D_criterion(old)
# Drummond function
D_D_e = bennu_ephemeris.D_criterion(old, version='d')
# hybrid
#D_HYB_e = bennu_ephemeris.D_criterion(meteor_obj, version='h')

# Southworth & Hawkins function
D_SH_fhu = bennu_from_horizon_updated.D_criterion(old)
# Drummond function
D_D_fhu = bennu_from_horizon_updated.D_criterion(old, version='d')
# hybrid
#D_HYB_fhu = bennu_ephemeris.D_criterion(meteor_obj, version='h')

print("\n-------------")

print("\nFROM HORIZONS (LATEST EPOCH) - 2460460.2864766")
print('D_SH', D_SH_fhu)
print('D_D', D_D_fhu)
#print('D HYBRID', D_HYB_e)

print("\nEPHEMERIS - WEB APP - 2455562.5")
print('D_SH', D_SH_e)
print('D_D', D_D_e)
#print('D HYBRID', D_HYB_fhu)

print("\nDifference")
print("D_SH", abs(D_SH_e - D_SH_fhu))
print("D_D", abs(D_D_e - D_D_fhu))
print("-------------")
'''
# NEW
print()
print("NEW")

D_SH = itokawa.D_criterion(new)
# Drummond function
D_D = itokawa.D_criterion(new, version='d')

print('D_SH', D_SH)
print('D_D', D_D)
'''
# Southworth & Hawkins function
D_SH_e = bennu_ephemeris.D_criterion(new)
# Drummond function
D_D_e = bennu_ephemeris.D_criterion(new, version='d')
# hybrid
#D_HYB_e = bennu_ephemeris.D_criterion(meteor_obj, version='h')

# Southworth & Hawkins function
D_SH_fhu = bennu_from_horizon_updated.D_criterion(new)
# Drummond function
D_D_fhu = bennu_from_horizon_updated.D_criterion(new, version='d')
# hybrid
#D_HYB_fhu = bennu_ephemeris.D_criterion(meteor_obj, version='h')

print("\n-------------")

print("\nFROM HORIZONS (LATEST EPOCH) - 2460460.2864766")
print('D_SH', D_SH_fhu)
print('D_D', D_D_fhu)
#print('D HYBRID', D_HYB_e)

print("\nEPHEMERIS - WEB APP - 2455562.5")
print('D_SH', D_SH_e)
print('D_D', D_D_e)
#print('D HYBRID', D_HYB_fhu)

print("\nDifference")
print("D_SH", abs(D_SH_e - D_SH_fhu))
print("D_D", abs(D_D_e - D_D_fhu))
print("-------------")
'''