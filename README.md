----------------------------------------
GMN Datamining
----------------------------------------
----------------------------------------
Vanessa Tran
----------------------------------------

Summer 2024 (May 1st - Aug 14th)

Supervisor: Dr. Paul Wiegert

----------------------------------------

Resources

- Global Meteor Network
  - https://globalmeteornetwork.org/data/traj_summary_data/
  - https://globalmeteornetwork.org/data/media/GMN_orbit_data_columns.pdf
- sbpy : https://sbpy.org/
- Astropy : https://www.astropy.org/
- Skyfit2 : https://aquarid.physics.uwo.ca/wiki/SkyFit2
- Horizons System : https://ssd.jpl.nasa.gov/horizons/app.html#/ , https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=bennu&view=VOP
- Rebound : https://rebound.readthedocs.io/en/latest/

Created Resources

- Google Docs (links)
  - How-To : Access files for GMN for Datamining : https://docs.google.com/document/d/1EgE0Rqx7c11TVZOLZIWc-IrsZfIjNUAcDOCpoY1fZ-8/edit?usp=sharing
  - Interstellar Filtering Method : https://docs.google.com/document/d/1kWUdP1ABZcQ4b9vL1sLGqWzPgsjD0CX5LdVWTRhYIgk/edit?usp=sharing
- Excel (.xlsx)
  - Potential Interstellars
  - Interstellar Reductions Stats (**outcomes!)
  - Asteroids of Interest 

-----------------------------------------

Code

- functions.py
  - all general functions organized by category (interstellar, orbital)
  - condition checking, wrapping angles, etc.

INTERSTELLAR

- gmn_interstellar_analysis.py
  - code to search for interstellar meteors
  - conditions can be specified in conditions list
 
- get_npuv_and_dvals.py
  - function: get the number per unit volume of meteors in a 5d space

ORBITAL

- orbital_elements_analysis.py
  - class for getting all relevant orbital elements (and filtering) to check for all relevant meteors for a check
  - used with d_value_meteor_class.py

- d_value_meteor_class.py
  - CLASS for Bennu meteor orbital element to get d value
  - adapted from the Orbit class from sbpy (child class, changes to work with self and obj instead of only Horizons data)
 
- semi_major_axis_filtering.py
  - checking for a normal distribution for GMN meteors that have a semi-major axis of around 1

- gmn_rebound_simulations.py
  - create 100 clones to see if the d values decrease over time
 
- gmn_reduced_ast_mets_check.py
  - check for the orbital element differences for the same meteor after manual reduction in skyfit2

