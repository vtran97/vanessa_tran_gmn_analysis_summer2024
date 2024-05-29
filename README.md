----------------------------------------
GMN Datamining
----------------------------------------

Vanessa Tran
----------------------------------------

Summer 2024 (May 1st - Aug 16th)

Supervisor: Dr. Paul Wiegert

----------------------------------------

Resources


- How-To : Access files for GMN for Datamining : https://docs.google.com/document/d/1EgE0Rqx7c11TVZOLZIWc-IrsZfIjNUAcDOCpoY1fZ-8/edit?usp=sharing
  - updated 2024-05-28
- sbpy : https://sbpy.org/
- Horizons System : https://ssd.jpl.nasa.gov/horizons/app.html#/ , https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=bennu&view=VOP

-----------------------------------------

Files


- gmn_interstellar_analysis.py
  - code to search for interstellar meteors
  - conditions can be specified in conditions list

- get_all_months.py
  - function to get all data from all monthly files GMN
 
- orbital_elements.py
  - class for getting all relevant orbital elements (and filtering) to check for all relevant meteors for a check
  - used with d_value_meteor_class.py

- d_value_meteor_class.py
  - class for Bennu meteor orbital element to get d value
  - class adapted from the Orbit class from sbpy
 
