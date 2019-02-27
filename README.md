# ci-calculator
## Problem
Some psychodiagnostic instruments don't offer confidence intervals for their norm values although the report of confidence intervals should be mandatory when reporting psychodiagnostic test results.
## Solution
This software calculates a confidence interval for a given norm value. The output is then visualized by plotting the confidence interval and the corresponding hypothetical norm value distribution. 

To do the calculation the following additional information has to be added by the user:
- reliability value (such as test-retest-reliability or internal consistency) 
- standard deviaton of the norm value (e.g. '15' for IQ tests)
- mean of the norm values (e.g. '100' for IQ tests)
- confidence level (user can choose between the following confidence levels: 99%, 95%, 90%, 80%)
- test type (one-sided or two-sided)
- hypothesis (equivalence hypothesis or regression towards the mean hypothesis)
