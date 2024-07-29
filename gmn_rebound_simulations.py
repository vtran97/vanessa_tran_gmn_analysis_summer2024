'''
Rebound Simulations 
Vanessa Tran

Does the D value reduce over time? 

Process Notes:

The orbit from GMN is automatically computed for an earlier time 60 days before impact. 
    ** The effect of the Earth's gravity in pulling the meteor in (and changing the meteor's original orbit) has 
    already been accounted for. This means that when you start the simulation of the meteor
    - you should actually use the orbital elements for Bennu, the planets, etc as they were 60 days 
    *before* the meteor actually occured
'''

# Imports

from datetime import datetime, timedelta
import rebound as rb
import numpy as np
import pandas as pd
from d_value_meteor_class import Meteor, Meteor_With_Uncertainties
import math
import matplotlib.pyplot as plt
import random

plt.rcParams.update({'font.size':30})

# date setup

def get_date_from_identifier(meteor_obj):
    identifier_list = list(meteor_obj.identity)
    year_sep = identifier_list[0:4]
    year = "".join(year_sep)
    #print(year)
    month_sep = identifier_list[4:6]
    month = "".join(month_sep)
    #print(month)
    day_sep = identifier_list[6:8]
    day = "".join(day_sep)
    #print(day)

    #identifier_date = str(year) + "/" + str(month) + "/" + str(day)
    identifier_date = datetime(year=int(year), month=int(month), day=int(day))
    return identifier_date

def get_date_sixty_days_before(meteor_obj):
    date = get_date_from_identifier(meteor_obj)
    day_delta = timedelta(days=-60) 
    date_sixty_days_before = date + day_delta 
    formatted = date_sixty_days_before.strftime("%Y-%m-%d")
    return formatted

# simulating meteors

def simulate_one_meteoroid(meteor_obj, goal_asteroid, date, simulation_end_time):
    """Given a meteoroid's parameters, simulate that meteoroid's evolutional history"""
    # note that the date given should be the one from 60 days before the date of the meteor

    print("\n***************************************")
    print("ENTER SIMULATION")
    print("***************************************\n")

    # Simulation setup and constants
    sim = rb.Simulation()
    #msun = rb.units.masses_SI["msun"]  # kg
    #m = m / msun  # convert meteoroid mass from kg to solar mass

    # Add solar system for the date of the meteor observation
    # Note that rebound uses G=1 by default so a year is 2pi, m is in solar masses although horizons objects need to be added in kg, 
    # position should be in AU and velocity in AU/year

    # Masses in solar masses
    sim.add("Sun", date=date, m=1.0, hash="Sun")
    sim.add("Mercury", date=date, m=1.6601141530543488e-07, hash="Mercury")
    sim.add("Venus", date=date, m=2.4478382877847715e-06, hash="Venus")
    sim.add("Geocenter", date=date, m=3.0034896149157645e-06, hash="Earth")
    #sim.add("Luna", date=date, m=3.694303310687701e-08, hash="Luna")
    sim.add("Mars", date=date, m=3.2271560375549977e-07, hash="Mars")
    sim.add("Jupiter", date=date, m=0.0009547919152112404, hash="Jupiter")
    sim.add("Saturn", date=date, m=0.0002858856727222417, hash="Saturn")
    sim.add("Uranus", date=date, m=4.36624373583127e-05, hash="Uranus")
    sim.add("Neptune", date=date, m=5.151383772628674e-05, hash="Neptune")

    sim.add(str(goal_asteroid.identity), date=date, m=float(goal_asteroid.mass), hash=str(goal_asteroid.identity))

    ps = sim.particles # ps is an array of pointers and will change as the simulation runs

    # testing
    '''print("a", meteor_obj.a)
    print("e", meteor_obj.e)
    print("i", math.radians(meteor_obj.i))
    print("node", math.radians(meteor_obj.node))
    print("peri", math.radians(meteor_obj.peri))
    print('mean anomaly', math.radians(meteor_obj.mean_anomaly))'''

    # To start the meteoroid in the right spot, we need to feed in x,y,z barycentric position in AU, velocity in AU/year divided by 2pi
    sim.add(a=meteor_obj.a, e=meteor_obj.e, inc=math.radians(meteor_obj.i), Omega=math.radians(meteor_obj.node), 
            omega=math.radians(meteor_obj.peri), M=math.radians(meteor_obj.mean_anomaly), hash="Meteoroid")
    '''sim.add(a=meteor_obj.a, e=meteor_obj.e, inc=math.radians(meteor_obj.i), Omega=math.radians(meteor_obj.node), 
            omega=math.radians(meteor_obj.peri),hash="Meteoroid")'''

    print("Meteor orbit testing")
    print(ps["Meteoroid"].orbit(primary=ps["Sun"]))
    print(ps["Meteoroid"].orbit())

    # to integrate backwards, use negative timestep
    sim.dt = -0.01

    '''# Add radiation forces
    #print("adding radiation forces")
    rebx = reboundx.Extras(sim)
    rf = rebx.load_force("radiation_forces")
    rebx.add_force(rf)
    rf.params["c"] = rbxConstants.C
    Q_pr = 1  # valid for meteoroid size >> wavelength of radiation
    # meteoroid radius should be in m, density should be in kg/m^3
    ps["Meteoroid"].params["beta"] = rebx.rad_calc_beta(
        6.6743e-11, 3.0e8, msun, lum_sol, r, rho, Q_pr
    )'''

    '''# Add gravitational harmonics of Earth
    #print("adding gravitational harmonics")
    gh = rebx.load_force("gravitational_harmonics")
    rebx.add_force(gh)
    ps["Earth"].params["J2"] = J2
    ps["Earth"].params["J4"] = J4
    ps["Earth"].params["R_eq"] = RE_eq
    ps["Earth"].r = dmin  # set size of Earth
    ps["Luna"].r = dmin / 4  # set size of Moon'''

    #Nbod = sim.N
    sim.move_to_com()  # We always move to the center of momentum frame before an integration

    # simulation_end_time is the simulation endtime in normal years
    Noutputs = 10000

    year = 2.0 * np.pi  # One year in units where G=1s
    times = np.linspace(0, simulation_end_time*year, num=Noutputs)

    '''# Specify how simulation should resolve collision
    sim.collision = "direct"
    sim.collision_resolve = "merge"
    sim.collision_resolve_keep_sorted = 1
    sim.track_energy_offset = 1'''

    # Record keplerian orbital elements for meteoroid to determine origin 
    a_met, e_met, inc_met, node_met, peri_met, q_met, d_sh, d_d = (
        np.zeros(Noutputs),
        np.zeros(Noutputs),
        np.zeros(Noutputs),
        np.zeros(Noutputs),
        np.zeros(Noutputs),
        np.zeros(Noutputs),
        np.zeros(Noutputs),
        np.zeros(Noutputs),
    )

    a_goal_ast, e_goal_ast, inc_goal_ast, node_goal_ast, peri_goal_ast, q_goal_ast = (
        np.zeros(Noutputs),
        np.zeros(Noutputs),
        np.zeros(Noutputs),
        np.zeros(Noutputs),
        np.zeros(Noutputs),
        np.zeros(Noutputs),
    )

    '''# Record semimajor axis and inclination of jupiter's orbit for Tisserand calculation
    a_jup, inc_jup = np.zeros(Noutputs), np.zeros(Noutputs)'''
    # Record time
    output_year = np.zeros(Noutputs)

    # Integrate over time
    for i, time in enumerate(times):
        if i%500==0:
            print(f"loop iter = {i}, {time}")

        sim.integrate(time)

        # getting current cersion of the meteor
        
        # x[i] = ps["Meteoroid"].x
        # y[i] = ps["Meteoroid"].y
        # z[i] = ps["Meteoroid"].z
        e_met[i] = ps["Meteoroid"].orbit(primary=ps["Sun"]).e
        a_met[i] = ps["Meteoroid"].orbit(primary=ps["Sun"]).a
        inc_met[i] = ps["Meteoroid"].orbit(primary=ps["Sun"]).inc
        node_met[i] = ps["Meteoroid"].orbit(primary=ps["Sun"]).Omega
        peri_met[i] = ps["Meteoroid"].orbit(primary=ps["Sun"]).omega

        '''e_met[i] = ps["Meteoroid"].orbit().e
        a_met[i] = ps["Meteoroid"].orbit().a
        inc_met[i] = ps["Meteoroid"].orbit().inc
        node_met[i] = ps["Meteoroid"].orbit().Omega
        peri_met[i] = ps["Meteoroid"].orbit().omega'''

        q_met[i] = a_met[i] * (1-e_met[i])

        # getting current version of goal ast 

        e_goal_ast[i] = ps[str(goal_asteroid.identity)].orbit(primary=ps["Sun"]).e
        a_goal_ast[i] = ps[str(goal_asteroid.identity)].orbit(primary=ps["Sun"]).a
        inc_goal_ast[i] = ps[str(goal_asteroid.identity)].orbit(primary=ps["Sun"]).inc
        node_goal_ast[i] = ps[str(goal_asteroid.identity)].orbit(primary=ps["Sun"]).Omega
        peri_goal_ast[i] = ps[str(goal_asteroid.identity)].orbit(primary=ps["Sun"]).omega

        '''e_goal_ast[i] = ps[str(goal_asteroid.identity)].orbit().e
        a_goal_ast[i] = ps[str(goal_asteroid.identity)].orbit().a
        inc_goal_ast[i] = ps[str(goal_asteroid.identity)].orbit().inc
        node_goal_ast[i] = ps[str(goal_asteroid.identity)].orbit().Omega
        peri_goal_ast[i] = ps[str(goal_asteroid.identity)].orbit().omega'''

        q_goal_ast[i] = a_goal_ast[i] * (1-e_goal_ast[i])

        current_state_meteor = Meteor_With_Uncertainties(a=a_met[i],
                                                         e=e_met[i],
                                                         q=q_met[i],
                                                         i=math.degrees(inc_met[i]),
                                                         node=math.degrees(node_met[i]),
                                                         peri=math.degrees(peri_met[i]))

        current_state_goal_asteroid = Meteor_With_Uncertainties(a=a_goal_ast[i],
                                                                e=e_goal_ast[i],
                                                                q=q_goal_ast[i],
                                                                i=math.degrees(inc_goal_ast[i]),
                                                                node=math.degrees(node_goal_ast[i]),
                                                                peri=math.degrees(peri_goal_ast[i]))

        d_sh[i] = current_state_goal_asteroid.D_criterion(current_state_meteor)
        d_d[i] =current_state_goal_asteroid.D_criterion(current_state_meteor, 'd')

        '''a_jup[i] = ps["Jupiter"].orbit(primary=ps["Sun"]).a
        inc_jup[i] = ps["Jupiter"].orbit(primary=ps["Sun"]).inc'''
        output_year[i] = time / (2*np.pi)

    df = pd.DataFrame({"e_met": e_met, 
                       "a_met": a_met, 
                       "inc_met": inc_met, 
                       "node_met": node_met, 
                       "peri_met": peri_met, 
                       "q_met": q_met, 
                       "d_sh" : d_sh,
                       "d_d" : d_d,
                       "year": output_year})
    '''df["Q"] = df["a_met"] * (1 + df["e_met"])
    df.loc[df["inc_met"] > (0.5*np.pi), "inc_met"] = np.abs(df["inc_met"] - np.pi)
    df.loc[df["inc_jup"] > (0.5*np.pi), "inc_jup"] = np.abs(df["inc_jup"] - np.pi)
    df["P_met"] = df["P_met"] / (2*np.pi)'''
    return df

def simulate_meteor_clone(meteor_obj, goal_asteroid, date, simulation_end_time):
    '''take uncertainties given for meteor and create clones'''

    # getting all the original values and finding the uncertainties 

    original_a = meteor_obj.a
    original_e = meteor_obj.e
    original_i = meteor_obj.i
    original_q = meteor_obj.q
    original_node = meteor_obj.node
    original_peri = meteor_obj.peri

    a_sigma = meteor_obj.a_sigma
    e_sigma = meteor_obj.e_sigma
    i_sigma = meteor_obj.i_sigma
    q_sigma = meteor_obj.q_sigma
    node_sigma = meteor_obj.node_sigma
    peri_sigma = meteor_obj.peri_sigma

    # getting the new randomized values within the uncertainties 

    if a_sigma != 0:
        new_a = original_a + random.uniform(-a_sigma, a_sigma)
    else:
        new_a = original_a

    if e_sigma != 0:
        new_e = original_e + random.uniform(-e_sigma, e_sigma)
    else:
        new_e = original_e

    if i_sigma != 0:
        new_i = original_i + random.uniform(-i_sigma, i_sigma)
    else:
        new_i = original_i

    if q_sigma != 0:
        new_q = original_q + random.uniform(-q_sigma, q_sigma)
    else:
        new_q = original_q

    if node_sigma != 0:
        new_node = original_node + random.uniform(-node_sigma, node_sigma)
    else:
        new_node = original_node

    if peri_sigma != 0:
        new_peri = original_peri + random.uniform(-peri_sigma, peri_sigma)
    else:
        new_peri = original_peri

    # new meteor obj

    clone = Meteor_With_Uncertainties(a=new_a,
                                        e=new_e, 
                                        i=new_i, 
                                        q=new_q,
                                        node=new_node,
                                        peri=new_peri)
    
    print("*******************************")
    print("CLONE")
    clone.get_attr()
    print("*******************************")

    clone_df = simulate_one_meteoroid(clone, goal_asteroid, date, simulation_end_time)

    return clone_df

# ------------------------------------------------------------------------------------------------------------------------------

# all values are taken directly from GMN, values in deg will be converted later
bennu = Meteor_With_Uncertainties(identity="Bennu", 
                                  a=1.1263910258948120, 
                                  e=0.2037450762416414,  
                                  q=0.8968944004459729, 
                                  i=6.03494377024794, 
                                  node=2.06086619569642, 
                                  peri=66.22306084084298, 
                                  mean_anomaly=101.7039520024729, 
                                  mass=3.6857483391753e-20) 

testing_meteor = Meteor_With_Uncertainties(identity="20211004095332_z6QQZ", 
                                           a=1.191079, 
                                           a_sigma=0.0047,
                                           e=0.230653,
                                           e_sigma=0.0012,
                                           q=0.916353,
                                           q_sigma=0.0039,
                                           i=9.042124,
                                           i_sigma=0.0427,
                                           node=11.102790,
                                           node_sigma=0,
                                           peri=56.491035,
                                           peri_sigma=1.4337,
                                           mean_anomaly=323.482034)

'''testing_meteor_2 = Meteor_With_Uncertainties(identity="20231012130023_GhSWo", 
                                           a=1.205943, 
                                           e=0.248383,
                                           q=0.906407,
                                           i=6.428566,
                                           node=18.615142,
                                           peri=57.440986,
                                           mean_anomaly=324.184028)'''

#-------------------------------------------------------------------------------------------------------------------------

# NUMBER OF CLONES
number_of_clones = 100

print("***************************************")
print("main asteroid")
testing_meteor.get_attr()
print("***************************************\n\n***************************************")
testing_date_start = get_date_sixty_days_before(testing_meteor)
print('testing date', testing_date_start)
print("***************************************\n")
testing_sim_end_time = 10000

for i in range(number_of_clones):
    simtest = simulate_meteor_clone(testing_meteor, bennu, testing_date_start, testing_sim_end_time)

    # TESTING GRAPHS 

    # D_SH
    ax = simtest.plot.scatter(x='year', y='d_sh', 
                                title="Bennu Test with D_SH: 20211004095332_z6QQZ")
    plt.grid()
    plt.show()

    # DD
    ax = simtest.plot.scatter(x='year', y='d_d', 
                                title="Bennu Test with D_D: 20211004095332_z6QQZ")
    plt.grid()
    plt.show()

'''simtest = simulate_one_meteoroid(testing_meteor, bennu, testing_date_start, testing_sim_end_time)
print(simtest)'''

'''# testing second meteor

print("***************************************")
print("getting attrs outside of function")
testing_meteor_2.get_attr()
print("***************************************")
testing_date_start = get_date_sixty_days_before(testing_meteor_2)
print('testing date', testing_date_start)
print("***************************************")
testing_sim_end_time = 100000

simtest = simulate_one_meteoroid(testing_meteor, bennu, testing_date_start, testing_sim_end_time)
print(simtest)'''



