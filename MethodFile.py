#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Modified: Monday July 20, 2020

@author: sarahzeichner
@author: guannondong

This is  the parallel file to the MethodFile object that exists in C# to talk to the Raw File reader, 
except this one is for data processing and creation of method File itself. Any changes to this file
should be cross correlated with the C# code
"""

import Peak

METHOD_FILE_NAME = "method.txt"

INPUT_PEAK_NUMBER = "peakNumber"
CHEMICAL_FORMULA_STRING = "chemicalFormula"
EXACT_MASS_STRING = "mass"
TOLERANCE_STRING = "tolerance"
TOLERANCE_UNITS_STRING = "toleranceUnits"
ISOTOPE_LIST_STRING = "isotopeList"
ELUTION_CURVE_ON_STRING = "elutionOn"
WEIGHTED_AVG_ON_STRING = "weightedAvgOn"
CSV_OUTPUT_ON_STRING = "csvOutputOn" 
CSV_OUTPUT_PATH_STRING = "csvOutputPath"
    
def ReadMethodFile(path):
    '''
    Read method file from input path 

    Input: path to method file
    Output: method file object
    '''
    peaks = []
    methodDictionary = {}
    with open(path) as f:
        methodLines = f.readlines()
        for line in range(len(methodLines)):
            thisLine = methodLines[line].split('=')
            thisKey = thisLine[0]
            thisVal = thisLine[1]
            methodDictionary[thisKey] = thisVal

    masses = methodDictionary[EXACT_MASS_STRING]
    tolerances = methodDictionary[TOLERANCE_STRING]
    toleranceUnits = methodDictionary[TOLERANCE_UNITS_STRING]
        
    for mass in range(len(masses)):
        peaks.append(masses[mass], tolerances[mass], toleranceUnits[mass])

    methodFile = MethodFile(inputPeaks=peaks, isotopeList=methodDictionary[ISOTOPE_LIST_STRING], elutionCurveOn=methodDictionary[ELUTION_CURVE_ON_STRING], weightedAvgOn=methodDictionary[WEIGHTED_AVG_ON_STRING], csvOutputOn = methodDictionary[CSV_OUTPUT_ON_STRING], csvOutputPath = methodDictionary[CSV_OUTPUT_PATH_STRING])

    return methodFile

class MethodFile:
    def __init__(self, inputPeaks, isotopeList, elutionCurveOn=False, weightedAvgOn=False, csvOutputOn = False, csvOutputPath = "output.csv"):
        self.peaks = inputPeaks
        self.isotopeList = []
        self.elutionCurveOn = elutionCurveOn
        self.weightedAvgOn = weightedAvgOn
        self.csvOutputOn = csvOutputOn
        self.csvOutputPath = csvOutputPath

    def WriteMethodFile(self, csvOutputOn = False, csvOutputPath="output.csv"):
        '''
        Write a method file object to a csv
        Inputs: Method File object
        Outputs: method file is written out to local directory
        '''
        f = open(METHOD_FILE_NAME,"w")

        peaks = self.peaks

        f.write(INPUT_PEAK_NUMBER + "=" + str(len(peaks)))

        f.write(EXACT_MASS_STRING + "=")
        for thisPeak in peaks:
            f.write("{0},".format(thisPeak.mass))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")
    
        f.write(TOLERANCE_STRING + "=")
        for thisPeak in peaks:
            f.write("{0},".format(thisPeak.mtol))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")
    
        f.write(TOLERANCE_UNITS_STRING + "=")
        for thisPeak in peaks:
            f.write("{0},".format(thisPeak.unit))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")

        f.write(ISOTOPE_LIST_STRING + "=")
        for thisIsotope in self.isotopeList:
            f.write("{0},".format(thisIsotope))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")    
 
        f.write(ELUTION_CURVE_ON_STRING+ "={0}\n".format(self.elutionCurveOn))
        f.write(WEIGHTED_AVG_ON_STRING + "={0}\n".format(self.weightedAvgOn))
        f.write(CSV_OUTPUT_ON_STRING + "={0}\n".format(self.csvOutputOn))
        f.write(CSV_OUTPUT_PATH_STRING + "={0}\n".format(self.csvOutputPath))

        f.close()
    
    def GetPeaks(self):
        '''
        Get peaks from input method dictionary
        Output: list of Peaks
        '''
        return self.peaks
