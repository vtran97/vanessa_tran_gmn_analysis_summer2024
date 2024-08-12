'''
GMN datamining 

Vanessa Tran (vtran97@uwo.ca)
May 1st to August 16 (2024)

Meteor class for checking against other asteroid orbital elemnts and orbit
- init takes in identity name (can be used for hash)
- prints attributes 
- get D criterion **adapted for manually inputted GMN data
    - Drummond
    - Southworth-Hawkins
    - Hybrid (not used)

Meteor with Uncertainties Class
- used for rebound clones -- same methods, more attributes in the init
'''

# -------------------------------------------
# imports - DO NOT DELETE!!!

import numpy as np
import astropy.units as u

#--------------------------------------------
# meteor class

class Meteor:

    def __init__(self, identity, e, q, i, node, peri):
        self.identity = identity
        self.e = e
        self.q = q
        self.i = i
        self.node = node
        self.peri = peri

    def get_attr(self):
        '''print all attributes'''
        print('identity :', self.identity)
        print('e =', self.e)
        print('q =', self.q)
        print('i =', self.i)
        print('node =', self.node)
        print('peri =', self.peri)
    
    def D_criterion(self, obj, version='sh'):
        '''
        THIS FUNCTION IS ADAPTED FROM ORIGINAL FUNCTION FROM SBPY !!! using self and obj instead 
        # of strictly orbit class that takes info from Horizons 
        # -- Mommert, Kelley, de Val-Borro, Li et al. (2019), Journal of Open Source Software, 4(38), 1426

        Evaluate orbit similarity D-criterion

        Three different versions of D-criterion are defined and often compared
        to each other, includingthe Southworth-Hawkins function [SH63]_,
        Drummond function [D81]_, and the hybrid version [J93]_.  See review by
        [W19]_.

        Parameters
        ----------
        obj : `~Orbit` object
            Object(s) against which to calculate D-criterion
        version : ['sh', 'd', 'h'], optional
            Select the versions of D-criterion formula.  Case insensitive.
            'sh' : Southworth-Hawkins function
            'd' : Drummond function
            'h' : hybrid function
            See references for the details of each version.

        Returns
        -------
        float or numpy.ndarray

        References
        ----------
        .. [SH63] `Southwarth, R. B., & Hawkins, G. S. 1963, SCoA, 7, 261
           <https://ui.adsabs.harvard.edu/abs/1963SCoA....7..261S/abstract>`_

        .. [D81] `Drummond, J. D. 1981, Icarus 45, 545
           <https://ui.adsabs.harvard.edu/abs/1981Icar...45..545D/abstract>`_

        .. [J93] `Jopek, T. J. 1993, Icarus 106, 603
           <https://ui.adsabs.harvard.edu/abs/1993Icar..106..603J/abstract>`_

        .. [W19] `Williams, I. P., Jopek, T. J., Rudawska, R., Tóth, J.,
           Kornoš, L. 2019, In: Ryabova, G. O., Asher, D. J., Compbell-Brown
           M. D., eds.), Cambridge, UK: Cambridge University Press, 210-234.
           <https://ui.adsabs.harvard.edu/abs/2019msme.book..210W/abstract>`_

        '''

        # sh --> southwarth-hawkins fn, d --> drummond fn
        if version.lower() not in ['sh', 'd', 'h']:
            raise ValueError("version should be one of ['sh', 'd', 'h'] (case "
                             "insensitive, {} received".format(version))

        # some prelim calcs
        diff_e = obj.e - self.e 
        sum_e = self.e + obj.e
        diff_q = obj.q - self.q 
        sum_q = self.q + obj.q 
        diff_i = (obj.i - self.i) * u.deg
        sum_i = (self.i + obj.i) * u.deg
        diff_node = (obj.node - self.node) * u.deg
        diff_peri = (obj.peri - self.peri ) * u.deg

        sin_i2 = np.sin(diff_i / 2)**2 \
            + np.sin(self.i * u.deg) * np.sin(obj.i * u.deg) * np.sin(diff_node / 2)**2

        if version.lower() == 'd':
            # Drummond function
            
            i_ba = np.arcsin(np.sqrt(sin_i2)) * 2

            beta_obj = np.arcsin(np.sin(obj.i * u.deg) * np.sin(obj.peri * u.deg))
            beta_self = np.arcsin(np.sin(self.i * u.deg) * np.sin(self.peri * u.deg))

            lamb_obj = obj.node * u.deg + np.arctan(np.cos(obj.i * u.deg) * np.tan(obj.peri * u.deg)) \
                + (np.cos(obj.peri * u.deg) < 0).astype(int) * np.pi * u.rad
            lamb_self = self.node * u.deg + np.arctan(np.cos(self.i * u.deg) * np.tan(self.peri * u.deg)) \
                + (np.cos(self.peri * u.deg) < 0).astype(int) * np.pi * u.rad

            theta_ba = np.arccos(np.sin(beta_obj) * np.sin(beta_self) + np.cos(beta_obj) \
                                 * np.cos(beta_self) * np.cos(lamb_obj - lamb_self))

            d2 = (diff_e / sum_e)**2 + (diff_q / sum_q)**2 \
                + (i_ba / (np.pi * u.rad))**2 \
                + (sum_e * theta_ba / (2 * np.pi * u.rad))**2
           
        else:
            cos_i2 = np.sqrt(1 - sin_i2)
            sign = (abs(diff_node) <= 180 * u.deg).astype(int) * 2 - 1
            pi_ba = diff_peri + 2 * sign * np.arcsin(
                np.cos(sum_i / 2) * np.sin(diff_node / 2) / cos_i2)

            if version.lower() == 'sh':
                # Southworth-Hawkins function
                d2 = diff_e**2 + (diff_q**2) + 4 * sin_i2 + (sum_e * np.sin(pi_ba / 2))**2

            else:
                # hybrid function
                #register(self.D_criterion, {'method': '1993Icar..106..603J'})
                d2 = diff_e**2 + (diff_q / sum_q)**2 + 4 * sin_i2 \
                    + (sum_e * np.sin(pi_ba / 2))**2
                
        d = np.sqrt(d2)
        return d
    
class Meteor_With_Uncertainties(Meteor):
    '''separate meteor class for the rebound simulations with meteor uncertainties'''

    def __init__(self, identity='', a=0, a_sigma=0, e=0, e_sigma=0, q=0, q_sigma=0, i=0, i_sigma=0, node=0, 
                 node_sigma=0, peri=0, peri_sigma=0, mean_anomaly=0, mass=0):
        
        self.identity = identity
        self.a = a
        self.a_sigma = a_sigma
        self.e = e
        self.e_sigma = e_sigma
        self.q = q
        self.q_sigma = q_sigma
        self.i = i
        self.i_sigma =  i_sigma
        self.node = node
        self.node_sigma = node_sigma
        self.peri = peri
        self.peri_sigma = peri_sigma
        self.mean_anomaly = mean_anomaly
        self.mass = mass

    def get_attr(self):
        print('identity :', self.identity)
        print('e =', self.e)
        print('e sigma =', self.e_sigma)
        print('q =', self.q)
        print('q sigma =', self.q_sigma)
        print('i =', self.i)
        print('i sigma =', self.i_sigma)
        print('node =', self.node)
        print('node sigma =', self.node_sigma)
        print('peri =', self.peri)
        print('peri sigma =', self.peri_sigma)
    
#----------------------------TESTS----------------------------

'''# Asteroid(e, q, i, node [NODE], w [PERI])

bennu = Meteor('bennu', .2037450762416414, .8968944004459729, 6.03494377024794, 2.06086619569642, 66.22306084084298) # taken from Horizons
ba14 = Meteor('ba14', .6662529585051395, 1.008577198658916, 18.91867269133972, 180.5336813221037, 351.8967232772523)
p_ast = Meteor('p_ast', .6730850153945767, .9960459017518296, 10.42219597127401, 190.9484957698451, 343.3104746438897)
abc = Meteor('abc', 0.4154170571173557, 2.50646576, 3.79647861, 29.96204163, 312.33501099)

# Asteroid(a, e, q, i, node [NODE], w [PERI]) + sigmas 

BENNU_TEST = Meteor_With_Uncertainties("Bennu", 1.1263910258948120, 0, .2037450762416414, 0, .8968944004459729, 0, 6.03494377024794, 0, 2.06086619569642, 0, 66.22306084084298, 0) 

BENNU_TEST.get_attr()

# Southworth & Hawkins function
D_SH = bennu.D_criterion(ba14) 
# Drummond function
D_D = bennu.D_criterion(ba14, version='d')

print()
print("BIGTEST")
print("*************************")
print('d_sh', D_SH)
print("*************************")
print("d_d", D_D)
print("*************************")
'''