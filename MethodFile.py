#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Modified: Thurs July 16 2020

@author: sarahzeichner
@author: guannondong

This is  the parallel file to the MethodFile object that exists in C# to talk to the Raw File reader, 
except this one is for data processing and creation of method File itself. Any changes to this file
should be cross correlated with the C# code
"""
#import dependencies
import Peak

#Global variables for method file
inputPeakNumberString = "peakNumber"
chemicalFormulaString = "chemicalFormula"
massString = "mass"
toleranceString = "tolerance"
toleranceUnitsString = "toleranceUnits"

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
        f = open("method.txt","w")

        peaks = self.peaks

        f.write("peakNumber={0}\n".format(len(peaks)))

        f.write(massString + "=")
        for thisPeak in peaks:
            f.write("{0},".format(thisPeak.mass))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")
    
        f.write(toleranceString + "=")
        for thisPeak in peaks:
            f.write("{0},".format(thisPeak.mtol))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")
    
        f.write(toleranceUnitsString + "=")
        for thisPeak in peaks:
            f.write("{0},".format(thisPeak.unit))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")

        f.write("isotopeList" + "=")
        for thisIsotope in self.isotopeList:
            f.write("{0},".format(thisIsotope))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")    
 
        f.write("elutionCurveOn={0}\n".format(self.elutionCurveOn))
        f.write("weightedAvgOn={0}\n".format(self.weightedAvgOn))
        f.write("csvOutputOn={0}\n".format(self.csvOutputOn))
        f.write("csvOutputPath={0}\n".format(self.csvOutputPath))

        f.close()

    def ReadMethodFile(self, path):
        '''
        Read method file from input path 

        Input: path to method file
        Output: dictionary containing method information
        '''
        methodDictionary = []
        with open(path) as f:
            methodLines = f.readlines()
            for line in range(len(methodLines)):
                thisLine = methodLines[line].split('=')
                thisKey = thisLine[0]
                thisVal = thisLine[1]
                methodDictionary[thisKey] = thisVal
        return methodDictionary
    
    def GetPeaks(self, methodDictionary):
        '''
        Get peaks from input method dictionary

        Input: method dictionary
        Output: list of Peaks
        '''
        peaks = []
        
        #TODO: Loop through dictionary and get a list of peaks
        
        return peaks


