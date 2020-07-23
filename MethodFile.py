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

class MethodFile:
    def __init__(self, inputPeaks, isotopeList, elutionCurveOn=False, weightedAvgOn=False, csvOutputOn = False, csvOutputPath = "output.csv"):
        self.peaks = inputPeaks
        self.isotopeList = []
        self.elutionCurveOn = elutionCurveOn
        self.weightedAvgOn = weightedAvgOn
        self.csvOutputOn = csvOutputOn
        self.csvOutputPath = csvOutputPath

        self.methodFileName = "method.txt"

        self.inputPeakNumberString = "peakNumber"
        self.chemicalFormulaString = "chemicalFormula"
        self.massString = "mass"
        self.toleranceString = "tolerance"
        self.toleranceUnitsString = "toleranceUnits"
        self.isotopeListString = "isotopeList"
        self.elutionCurveOnString = "elutionOn"
        self.weightedAvgOnString = "weightedAvgOn"
        self.csvOutputOnString = "csvOutputOn" 
        self.csvOutputPathString = "csvOutputPath"
    
    def WriteMethodFile(self, csvOutputOn = False, csvOutputPath="output.csv"):
        '''
        Write a method file object to a csv
        Inputs: Method File object
        Outputs: method file is written out to local directory
        '''
        f = open(self.methodFileName,"w")

        peaks = self.peaks

        f.write(self.inputPeakNumberString + "=" + str(len(peaks)))

        f.write(self.massString + "=")
        for thisPeak in peaks:
            f.write("{0},".format(thisPeak.mass))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")
    
        f.write(self.toleranceString + "=")
        for thisPeak in peaks:
            f.write("{0},".format(thisPeak.mtol))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")
    
        f.write(self.toleranceUnitsString + "=")
        for thisPeak in peaks:
            f.write("{0},".format(thisPeak.unit))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")

        f.write(self.isotopeListString + "=")
        for thisIsotope in self.isotopeList:
            f.write("{0},".format(thisIsotope))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")    
 
        f.write(self.elutionCurveOnString + "={0}\n".format(self.elutionCurveOn))
        f.write(self.weightedAvgOnString + "={0}\n".format(self.weightedAvgOn))
        f.write(self.csvOutputOnString + "={0}\n".format(self.csvOutputOn))
        f.write(self.csvOutputPathString + "={0}\n".format(self.csvOutputPath))

        f.close()

    def ReadMethodFile(self, path):
        '''
        Read method file from input path 

        Input: path to method file
        Output: dictionary containing method information
        '''
        methodDictionary = {}
        with open(path) as f:
            methodLines = f.readlines()
            for line in range(len(methodLines)):
                thisLine = methodLines[line].split('=')
                thisKey = thisLine[0]
                thisVal = thisLine[1]
                methodDictionary[thisKey] = thisVal
        
        masses = methodDictionary[self.massString]
        tolerances = methodDictionary[self.toleranceString]
        toleranceUnits = methodDictionary[self.toleranceUnitsString]
        
        for mass in range(len(masses)):
            self.peaks.append(masses[mass], tolerances[mass], toleranceUnits[mass])

        self.isotopeList = methodDictionary[self.isotopeListString]
        self.elutionCurveOn = methodDictionary[self.elutionCurveOnString]
        self.weightedAvgOn = methodDictionary[self.weightedAvgOnString]
        self.csvOutputOn = methodDictionary[self.csvOutputOnString]
        self.csvOutputPath = methodDictionary[self.csvOutputPathString]

        return methodDictionary
    
    def GetPeaks(self):
        '''
        Get peaks from input method dictionary
        Output: list of Peaks
        '''
        return self.peaks


