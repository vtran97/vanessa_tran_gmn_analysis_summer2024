'''
GMN datamining 

Vanessa Tran (vtran97@uwo.ca)
May 1st to August 16 (2024)

all functions
'''

#---------------------------------------------------------------------------------------------------------------
# general functions

'''
function : get all entries up to the current month 
this helps to automatically create a list of all the years in the system so that
you don't have to loop through them all manually (done by just making a bunch of lists and putting them
into one at the end, but long term this is not effective)
'''

# getting dates
from datetime import datetime

def get_all_months_by_year_list():
    # returns a list of all months that the GMN has been active -- used to acccess data through GMN database

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
            # special case, only one month and should never change (unless we build a time machine)
            all_months.append(['2018-12'])

        else:
            # for all months after leading up to current date for the current year 

            year_month_list = [] # full list
            cut_list = [] # list for the cut off year
            done = False # used for later for cut list

            for month in range(1, 13):

                if month in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    month_name = str(year) + '-0' + str(month)
                    year_month_list.append(month_name)

                else: # months 10, 11, 12
                    month_name = str(year) + "-" + str(month)
                    year_month_list.append(month_name)
            
            if year != int(current_month.split("-")[0]): # if the year is not the current year
                all_months.append(year_month_list)
            
            else: # if the year is the current year
                # need to shorten the lsit to find the months up to this point that we can analyse 
                # (not getting results from the future)

                while not done:
                    for i in range(len(year_month_list)):
                        if year_month_list[i] == current_month:
                            cut_list.append(year_month_list[i])
                            done = True
                        if year_month_list[i] != current_month and done == False:
                            cut_list.append(year_month_list[i])

                all_months.append(cut_list)

    # return list in form [[months from 2018], [months from 2019], [months from 2020], etc...]
    return all_months

#---------------------------------------------------------------------------------------------------------------
# interstellar functions

'''
check conditions for interstellar meteors
'''

def check_conditions_interstellar(value, value_cutoff,
                     vhel, vhel_cutoff, 
                     vhel_sigma,
                     vinit, vinit_cutoff):
    if value > value_cutoff and vhel_sigma !=0 and vhel > vhel_cutoff and vinit < vinit_cutoff:
        return True
    else:
        return False

'''
print output for potential interstellar meteors
'''

def print_output_interstellar(value=0, value_cutoff=5, 
                 vhel=0, vhel_cutoff=50, 
                 vhel_sigma=0, 
                 vinit=0, vinit_cutoff=50, 
                 qc=0, 
                 identifier="", 
                 stations='', 
                 skyfit_script_identifier=''):
    
    # length for the text splits
    cus_lens = [8,6]
    res = []
    start = 0

    # prints the output give the above parameters
    output = ""
    if value > value_cutoff and vhel > vhel_cutoff and vinit < vinit_cutoff:

        ''' 
        # not needed right now -- modified to never have sigma = 0 entries 
        if vhel_sigma_mod[number] == 0:
            output += "||SIGMA = ZERO|| "
        else:
            output += "                 "
        '''

        # identity of meteor in GMN database
        output += "||IDENTITY: " + str(identifier) + "|| "

        # vhel (heliocentric velocity) according to GMN
        txt = str(vhel)
        if len(txt) <= 7: # string too short
            while len(txt) != 7:
                txt = txt + '0'
        output += "||VHEL: " + txt + "|| "

        # the sigma (sd) of vhel in GMN
        if vhel_sigma != 0:
            txt = str(vhel_sigma)
            if len(txt) <= 6: # string too short
                while len(txt) != 6:
                    txt += '0'
            output += "||SIGMA (VHEL): " + txt + "|| "
        
        # the Qc (convergence angle) according to GMN 
        txt = str(qc)
        if len(txt) <= 5: # string too short
            while len(txt) != 5:
                txt = txt + '0'
        output += "||QC: " + txt + "|| "

        # computed value for the number of error bars above 42km/s the measure vhel is 
        txt = str(value)
        if len(txt) <= 18: # string too short
            while len(txt) != 18:
                txt = txt + '0'
        output += "||VALUE: " + txt + "|| "

        # specific format for raw data --> Denis Vida
        iden = str(identifier).split("_")[0]
        for size in cus_lens:
            res.append(iden[start : start + size])
            start += size
        txt = str(skyfit_script_identifier).split(".")[1]
        output += "\n\t\t||SCRIPT IDENTIFIER FOR RAW: " + res[0] + "_" + res[1] + "." + txt + "|| " 

        # stations involved in seeing the meteor
        txt = ''
        last = len(stations) - 1
        for station in range(len(stations)): # printing it nicely and not in list with ''
            if stations[station] != stations[last]:
                txt += stations[station] + ", "
            else:
                txt += stations[station]
        output += "||STATIONS: " + txt + "|| "

        print(output)

#---------------------------------------------------------------------------------------------------------------
# orbital elements functions

'''
wraps angles for conndition checking for elements that deal with degrees
'''

def wrap_angle(elem, elem_min, elem_max):

    if elem_min < 0:
        # editing the restrictions since angle covers interval before and after zero degrees
        elem_sub_min = 360 + elem_min
        elem_sub_max = 360
        # reset min to 0 for degrees
        elem_min = 0
        if elem > elem_min and elem < elem_max or elem < elem_sub_max and elem > elem_sub_min:
            return True
    elif elem_max > 360:
        elem_sub_min = 0
        elem_sub_max = elem_max - 360
        elem_max = 360
        if elem > elem_min and elem < elem_max or elem < elem_sub_max and elem > elem_sub_min:
            return True
    else:
        return False

'''
condition checking for all orbital elements 
'''

def check_conditions_orbital(a, active_a, a_min, a_max, 
                             e, active_e, e_min, e_max, 
                             i, active_i, i_min, i_max,
                             peri, active_peri, peri_min, peri_max,
                             node, active_node, node_min, node_max,
                             Pi, active_Pi, Pi_min, Pi_max,
                             b, active_b, b_min, b_max,
                             q, active_q, q_min, q_max,
                             f, active_f, f_min, f_max,
                             M, active_M, M_min, M_max,
                             Q, active_Q, Q_min, Q_max,
                             n, active_n, n_min, n_max,
                             T, active_T, T_min, T_max,
                             TisserandJ, active_TJ, TisserandJ_min, TisserandJ_max):
    '''checks for all orbital elements conditions -- optimize!!'''

    conditions_list = []

    if a > a_min and a < a_max or active_a == False:
        conditions_list.append(True)
    else:
        return False

    if e > e_min and e < e_max or active_e == False:
        conditions_list.append(True)
    else:
        return False
    
    if i > i_min and i < i_max and i_min > 0 and i_max < 360 or active_i == False:
        conditions_list.append(True)
    elif i_min < 0 or i_max > 360:
        if wrap_angle(i, i_min, i_max) == True:
            conditions_list.append(True)
    else:
        return False
    
    if peri > peri_min and peri < peri_max and peri_min >= 0 and peri_max <= 360 or active_peri == False:
        conditions_list.append(True)
    elif peri_min <= 0 or peri_max >= 360:
        if wrap_angle(peri, peri_min, peri_max) == True:
            conditions_list.append(True)
    else:
        return False

    if node > node_min and node < node_max and node_min >= 0 and node_max <= 360 or active_node == False:
        conditions_list.append(True)
    elif node_min <= 0 or node_max >= 360:
        if wrap_angle(node, node_min, node_max) == True:
            conditions_list.append(True)
    else:
        return False
  
    if Pi > Pi_min and Pi < Pi_max and Pi_min >= 0 and Pi_max <= 360 or active_Pi == False:
        conditions_list.append(True)
    elif Pi_min <= 0 or Pi_max >= 360:
        if wrap_angle(Pi, Pi_min, Pi_max) == True:
            conditions_list.append(True)
    else:
        return False

    if b > b_min and b < b_max and b_min >= 0 and b_max <= 360 or active_b == False:
        conditions_list.append(True)
    elif b_min <= 0 or b_max >= 360:
        if wrap_angle(b, b_min, b_max) == True:
            conditions_list.append(True)
    else:
        return False

    if q > q_min and q < q_max or active_q == False:
        conditions_list.append(True)
    else:
        return False

    if f > f_min and f < f_max and f_min >= 0 and f_max <= 360 or active_f == False:
        conditions_list.append(True)
    elif f_min <= 0 or f_max >= 360:
        if wrap_angle(f, f_min, f_max) == True:
            conditions_list.append(True)
    else:
        return False

    if M > M_min and M < M_max and M_min >= 0 and M_max <= 360 or active_M == False:
        conditions_list.append(True)
    elif M_min <= 0 or M_max >= 360:
        if wrap_angle(M, M_min, M_max) == True:
            conditions_list.append(True)
    else:
        return False

    if Q > Q_min and Q < Q_max or active_Q == False:
        conditions_list.append(True)
    else:
        return False
    
    if n > n_min and n < n_max or active_n == False:
        conditions_list.append(True)
    else:
        return False
    
    if T > T_min and T < T_max or active_T == False:
        conditions_list.append(True)
    else:
        return False
    
    if TisserandJ > TisserandJ_min and TisserandJ < TisserandJ_max or active_TJ == False:
        conditions_list.append(True)
    else:
        return False

    if len(conditions_list) == 14:
        return True