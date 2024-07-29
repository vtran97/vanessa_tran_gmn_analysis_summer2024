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
from gmn_orbital_elements_analysis import get_number_per_unit_volume

# for D values
from d_value_meteor_class import Meteor

# math
import math

plt.rcParams.update({'font.size':30})

#-------------------------------------------------------------------------------------------------------------

# function

def get_npuv_and_d_vals(name, conds, meteor_obj, mods):

    print("----------------------------------------------------------------------------------------------------")
    print(name)

    index = 0

    unit_per_volume_list = []
    volume_list = []

    get_npuv = get_number_per_unit_volume(mods, conds)
    dataframe = get_npuv[0]

    for idx in range(30):

        ndo5d = narrow_dataframe_orbital_5d(dataframe, mods, conds)
        if ndo5d[0] != 0:
            units_per_vol = len(ndo5d[1]) / ndo5d[0]
        else:
            units_per_vol = 0
        volume = ndo5d[0]

        unit_per_volume_list.append(units_per_vol)
        volume_list.append(volume)

        print()
        print("modifiers    :", mods)
        print('# candidates :', len(ndo5d[1]))
        print('volume       :', volume)
        print('# / v        :', units_per_vol)

        print('candidate list:', ndo5d[1])

        mods[0] -= 0.005 
        # this was orignially - 0.5, but is adaped for smaller i values = -= 0.025
        mods[1] -=  0.5

    # print(get_npuv[1])

    # try "true" asteroid values against all other potential asteroids
    for meteor_obj_np in get_npuv[1]:

    # Southworth & Hawkins function
        D_SH = meteor_obj_np.D_criterion(meteor_obj)
        # Drummond function
        D_D = meteor_obj_np.D_criterion(meteor_obj, version='d')

        print("\n-------------")
        meteor_obj_np.get_attr()

        print("\nD VALS")
        print('D_SH', D_SH)
        print('D_D', D_D)

    index += 1

    graph = plt.plot(volume_list, unit_per_volume_list, label=name)
    
    '''plt.xlabel("volume")
    plt.ylabel("number per unit volume")
    plt.title("npuv 5d (normal scale)")
    plt.grid()
    plt.show()'''
    '''
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
    plt.title("npuv 5d (ln)")
    plt.grid()
    plt.show()'''

# ===========================================================================================================
# swift tuttle testing
'''

# swift tuttle conds for 5d space
conds_swift_tuttle = [True, 26.0920694978266, 
                      True, 0.963225755046038,
                      True, 113.453816997171, 
                      True, 152.9821676305871,
                      True, 139.3811920815948]


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

#===================================================================================================================
'''
modifiers_5d = [0.2, 6]
conds_bennu = [True, 1.126391025894812, 
              True, 0.2037450762416414,
              True, 6.03494377024794, 
              True, 66.22306084084298,
              True, 2.06086619569642]

# Asteroid(e, q, i, omega [NODE], w [PERI])
bennu_ephemeris = Meteor('Bennu', 0.2037450762416414, 0.8968944004459729, 6.03494377024794, 2.06086619569642, 66.22306084084298) 
bennu_from_horizon_updated = Meteor('Bennu', 0.2037482514536186, 0.89654206, 6.03301417, 1.98511762, 66.37138491)
graphs = get_npuv_and_d_vals('Bennu Eph', conds_bennu, bennu_ephemeris, modifiers_5d)
modifiers_5d = [0.2, 6]
graphs = get_npuv_and_d_vals('Bennu Hor', conds_bennu, bennu_from_horizon_updated, modifiers_5d)
'''
#----------------------------------------------------
'''
# Eros
# make the largest interval and then narrow from there! --> for most 5d
modifiers_5d = [0.2,
                20]
# conditions for 5d space, a e i peri node
conds_eros = [True, 1.458177646485403, 
              True, 0.2227072743779392, 
              True, 10.82762857430502, 
              True, 178.8953167089443, 
              True, 304.2765731967428]
# Asteroid(e, q, i, omega [NODE], w [PERI])
eros = Meteor('Eros', 0.2227072743779392, 1.133430877277801, 10.82762857430502, 304.2765731967428, 178.8953167089443)
graphs = get_npuv_and_d_vals('Eros', conds_eros, eros, modifiers_5d)

# Itokawa
modifiers_5d = [0.2,
                20]
conds_itokawa = [True, 1.324142578587497,
                 True, 0.2803311777299725,
                 True, 1.621207668814055,
                 True, 162.8211329499564, 
                 True, 69.0761042651376]
itokawa = Meteor('Itokawa', 0.2803311777299725, 0.9529441300496611, 1.621207668814055, 69.0761042651376, 162.8211329499564)
graphs = get_npuv_and_d_vals('Itokawa', conds_itokawa, itokawa, modifiers_5d)

# Toutatis
modifiers_5d = [0.2,
                20]
conds_toutatis = [True, 2.543728029076248, 
                  True, 0.624758896480083, 
                  True, 0.4480680353844077, 
                  True, 277.868771555242, 
                  True, 125.3549352905831]
toutatis = Meteor('Toutatis', 0.624758896480083, 0.9545113126851149, 0.4480680353844077, 125.3549352905831, 277.868771555242)
graphs = get_npuv_and_d_vals('Toutatis', conds_toutatis, toutatis, modifiers_5d)

# Ryugu
modifiers_5d = [0.2,
                6]
conds_ryugu = [True, 1.191013624852465, 
               True, 0.1910659421644889,
               True, 5.866516749812472,
               True, 211.6156610065788,
               True, 251.2954193296629]
ryugu = Meteor('Ryugu', 0.1910659421644889, 0.963451484489286, 5.866516749812472, 251.2954193296629, 211.6156610065788)
graphs = get_npuv_and_d_vals('Ryugu', conds_ryugu, ryugu, modifiers_5d)

# Didymos
modifiers_5d = [0.2,
                20]
conds_didymos = [True, 1.64268149873718,
                 True, 0.3832302498647931,
                 True, 3.414222573974985,
                 True, 319.5916377730013,
                 True, 72.9867658813169]
didymos = Meteor('Didymos', 0.3832302498647931, 1.013156257527858, 3.414222573974985, 72.9867658813169, 319.5916377730013)
graphs = get_npuv_and_d_vals('Didymos', conds_didymos, didymos, modifiers_5d)

# KY26
modifiers_5d = [0.2,
                20]
conds_ky26 = [True, 1.232849543905062,
              True, 0.2018717279444665,
              True, 1.481016973751399,
              True, 209.363399906683,
              True, 84.36267152662202]
ky26 = Meteor('Didymos', 0.2018717279444665, 0.9839720761813993, 1.481016973751399, 84.36267152662202, 209.363399906683)
graphs = get_npuv_and_d_vals('KY26', conds_ky26, ky26, modifiers_5d)

# Kamo'oalewa
modifiers_5d = [0.2,
                20]
conds_kamo_oalewa = [True, 1.000942780042978,
                     True, 0.1026866211272175,
                     True, 7.796052783093273,
                     True, 305.047752740526,
                     True, 65.79070140817294]
kamo_oalewa = Meteor('Kamo`oalewa', 0.1026866211272175, 0.1026866211272175, 7.796052783093273, 65.79070140817294, 305.047752740526)
graphs = get_npuv_and_d_vals('Kamo`oalewa', conds_kamo_oalewa, kamo_oalewa, modifiers_5d)

# Cruithne
modifiers_5d = [0.2,
                20]
conds_cruithne= [True, 0.997751694813871,
                 True, 0.5148730506697846,
                 True, 19.8024438623418,
                 True, 43.88297234753313,
                 True, 126.1950905131228]
cruithne = Meteor('Cruithne', 0.5148730506697846, 0.4840362358941053, 19.8024438623418, 126.1950905131228, 43.88297234753313)
graphs = get_npuv_and_d_vals('Cruithne', conds_cruithne, cruithne, modifiers_5d)

# 2020 VL5
modifiers_5d = [0.2,
                20]
conds_vl5 = [True, 0.9990750251003194, 
             True, 0.2789646800281618,
             True, 1.736604995346983,
             True, 237.6861184521349,
             True, 279.2998965781997]
vl5 = Meteor('VL5', 0.2789646800281618, 0.7203683803990811, 1.736604995346983, 237.6861184521349, 279.2998965781997)
graphs = get_npuv_and_d_vals('VL5', conds_vl5, vl5, modifiers_5d)

# CC21
modifiers_5d = [0.2,
                20]
conds_cc21 = [True, 1.032326006473957,
              True, 0.2192516988918617,
              True, 4.80766125895221,
              True, 179.4306792644965,
              True, 75.45460154781179]
cc21 = Meteor('CC21', 0.2192516988918617, 0.8059867757442905, 4.80766125895221, 75.45460154781179, 179.4306792644965)
graphs = get_npuv_and_d_vals('CC21', conds_cc21, cc21, modifiers_5d)

# OD20 
modifiers_5d = [0.2,
                20]
conds_od20 = [True, 1.365180926068712,
              True, 0.3688584165103676,
              True, 4.192748788823585,
              True, 275.3530380796205,
              True, 259.8466961960187]
od20 = Meteor('od20', 0.3688584165103676, 0.8616224514288494, 4.192748788823585, 275.3530380796205, 259.8466961960187)
graphs = get_npuv_and_d_vals('OD20', conds_od20, od20, modifiers_5d)

# Xanthus
modifiers_5d = [0.2,
                20]
conds_xanthus = [True, 	1.041925587107289,
                 True, 0.2501708344732658,
                 True, 14.14449092874004,
                 True, 333.8280423148674,
                 True, 23.94756859751227]
xanthus = Meteor('Xanthus', 0.2501708344732658, 0.7812661935216111, 14.14449092874004, 333.8280423148674, 23.94756859751227)
graphs = get_npuv_and_d_vals('Xanthus', conds_xanthus, xanthus, modifiers_5d)

# Apophis
modifiers_5d = [0.2,
                20]
conds_apophis = [True, 0.922552140675628,
                True, 0.1912907261004625,
                True, 3.339736385186364,
                True, 126.6832317899634,
                True, 203.9153721810904]
apophis = Meteor('Apophis', 0.1912907261004625, 0.7460764718202511, 3.339736385186364, 203.9153721810904, 126.6832317899634)
graphs = get_npuv_and_d_vals('Apophis', conds_apophis, apophis, modifiers_5d)
'''
plt.xlabel("volume")
plt.ylabel("number per unit volume")
plt.title("npuv 5d (normal scale)")
plt.legend()
plt.grid()
plt.show()