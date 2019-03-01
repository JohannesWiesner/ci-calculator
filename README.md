# ci-calculator
The code is written in Python 3.6.2. The interface is written in German but can be easily adapted to any other language. 
## Problem
Some psychodiagnostic instruments don't offer confidence intervals for their norm values although the report of confidence intervals should be mandatory when reporting psychodiagnostic test results.
## Solution
This software calculates a confidence interval for a given norm value. The output is then visualized by plotting the confidence interval under the corresponding hypothetical norm value distribution. 

To do the calculation the following additional information has to be added by the user:
- reliability value (such as test-retest-reliability or internal consistency) 
- standard deviaton of the norm value (e.g. '15' for IQ tests)
- mean of the norm values (e.g. '100' for IQ tests)
- confidence level (user can choose between the following confidence levels: 99%, 95%, 90%, 80%)
- test type (one-sided or two-sided)
- hypothesis (equivalence hypothesis or regression towards the mean hypothesis)
## Create a standalone application using cx_Freeze
This repository includes the distutils setup script setup.py. After installing cx_Freeze you can create a standalone application using cx_Freeze and the provided setup.py script. Please note that cx_Freeze tends to produce quite large standalone applications and that the behavior of the setup.py script tends to be unclear sometimes. With the current setup.py script the application is around 200 MB big on my machine. The msi-installer file is around 90 MB big. Any help to reduce the size of the application is greatly appreciated.

For further information see [cx_Freeze documentation](https://cx-freeze.readthedocs.io/en/latest/)

## Projects
Online implementation of ci-calculator in [R-Shiny](https://shiny.rstudio.com/) is planned and will be linked here when finished.