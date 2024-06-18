'''
GMN datamining 

Vanessa Tran (vtran97@uwo.ca)
May 1st to August 16 (2024)

Meteor class for checking against other asteroid orbital elemnts and orbit
'''

# -------------------------------------------------------------------------------------
# imports - DO NOT DELETE!!!

import numpy as np
import astropy.units as u

#--------------------------------------------
# meteor class

class Meteor:

    def __init__(self, identity, e, q, i, omega, w):
        self.identity = identity
        self.e = e
        self.q = q
        self.i = i
        self.omega = omega
        self.w = w

    def get_attr(self):
        print('identity :', self.identity)
        print('e =', self.e)
        print('q =', self.q)
        print('i =', self.i)
        print('omega =', self.omega)
        print('w =', self.w)
        
    def D_criterion(self, obj, version='sh'):
        # THIS FUNCTION IS ADAPTED FROM ORIGINAL FUNCTION FROM SBPY !!! using self and obj instead 
        # of strictly orbit class that takes info from Horizons 
        # -- Mommert, Kelley, de Val-Borro, Li et al. (2019), Journal of Open Source Software, 4(38), 1426

        """Evaluate orbit similarity D-criterion

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

        """

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
        diff_omega = (obj.omega - self.omega) * u.deg
        diff_w = (obj.w - self.w ) * u.deg

        sin_i2 = np.sin(diff_i / 2)**2 \
            + np.sin(self.i * u.deg) * np.sin(obj.i * u.deg) * np.sin(diff_omega / 2)**2

        if version.lower() == 'd':
            # Drummond function
            
            i_ba = np.arcsin(np.sqrt(sin_i2)) * 2

            beta_obj = np.arcsin(np.sin(obj.i * u.deg) * np.sin(obj.w * u.deg))
            beta_self = np.arcsin(np.sin(self.i * u.deg) * np.sin(self.w * u.deg))

            lamb_obj = obj.omega * u.deg + np.arctan(np.cos(obj.i * u.deg) * np.tan(obj.w * u.deg)) \
                + (np.cos(obj.w * u.deg) < 0).astype(int) * np.pi * u.rad
            lamb_self = self.omega * u.deg + np.arctan(np.cos(self.i * u.deg) * np.tan(self.w * u.deg)) \
                + (np.cos(self.w * u.deg) < 0).astype(int) * np.pi * u.rad

            theta_ba = np.arccos(np.sin(beta_obj) * np.sin(beta_self) + np.cos(beta_obj) \
                                 * np.cos(beta_self) * np.cos(lamb_obj - lamb_self))

            d2 = (diff_e / sum_e)**2 + (diff_q / sum_q)**2 \
                + (i_ba / (np.pi * u.rad))**2 \
                + (sum_e * theta_ba / (2 * np.pi * u.rad))**2
           
        else:
            cos_i2 = np.sqrt(1 - sin_i2)
            sign = (abs(diff_omega) <= 180 * u.deg).astype(int) * 2 - 1
            pi_ba = diff_w + 2 * sign * np.arcsin(
                np.cos(sum_i / 2) * np.sin(diff_omega / 2) / cos_i2)

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
    
#----------------------------TESTS----------------------------

# Asteroid(e, q, i, omega [NODE], w [PERI])
'''
bennu = Meteor(.2037450762416414, .8968944004459729, 6.03494377024794, 2.06086619569642, 66.22306084084298) # taken from Horizons
ba14 = Meteor(.6662529585051395, 1.008577198658916, 18.91867269133972, 180.5336813221037, 351.8967232772523)
p_ast = Meteor(.6730850153945767, .9960459017518296, 10.42219597127401, 190.9484957698451, 343.3104746438897)
abc = Meteor(0.4154170571173557, 2.50646576, 3.79647861, 29.96204163, 312.33501099)

# Southworth & Hawkins function
D_SH = abc.D_criterion(ba14) 
# Drummond function
D_D = abc.D_criterion(ba14, version='d')

print()
print("BIGTEST")
print("*************************")
print('d_sh', D_SH)
print("*************************")
print("d_d", D_D)
print("*************************")
'''