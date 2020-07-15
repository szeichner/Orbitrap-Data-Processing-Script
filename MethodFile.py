#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Modified: Wed July 15 2020

@author: sarahzeichner
@author: guannondong

This is  the parallel file to the MethodFile object that exists in C#
"""

class MethodFile:
  def __init__(self, inputPeakNumber, masses, tolerances, isotopeList, elutionCurveOn=False, weightedAvgOn=False):
    self.inputPeakNumber = inputPeakNumber
    self.masses = masses
    self.tolerances = tolerances
    self.isotopeList = []
    self.elutionCurveOn = elutionCurveOn
    self.weightedAvgOn = weightedAvgOn

def _importMethodFile(path):
    with open(path) as f:
        methodLines = f.readlines()
        
    #populate method file with method lines
    return methodLines


inputPeakNumberString = "peakNumber"
chemicalFormulaString = "chemicalFormula"
massString = "mass"
toleranceString = "tolerance"
toleranceUnitsString = "toleranceUnits"