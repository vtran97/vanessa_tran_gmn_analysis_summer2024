----------------------------------------
GMN Datamining
----------------------------------------

Vanessa Tran
----------------------------------------

Summer 2024 (May 1st - Aug 14th)

Supervisor: Dr. Paul Wiegert

----------------------------------------

Resources


- How-To : Access files for GMN for Datamining : https://docs.google.com/document/d/1EgE0Rqx7c11TVZOLZIWc-IrsZfIjNUAcDOCpoY1fZ-8/edit?usp=sharing
  - updated 2024-05-28
- sbpy : https://sbpy.org/
- Horizons System : https://ssd.jpl.nasa.gov/horizons/app.html#/ , https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=bennu&view=VOP

-----------------------------------------

Files

- functions.py
  - all general functions organized by category (interstellar, orbital)
  - condition checking, wrapping angles, etc.

- gmn_interstellar_analysis.py
  - code to search for interstellar meteors
  - conditions can be specified in conditions list
 
- orbital_elements_analysis.py
  - class for getting all relevant orbital elements (and filtering) to check for all relevant meteors for a check
  - used with d_value_meteor_class.py

- d_value_meteor_class.py
  - CLASS for Bennu meteor orbital element to get d value
  - adapted from the Orbit class from sbpy (child class, changes to work with self and obj instead of only Horizons data)
 
