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
        Inputs:
        Outputs:

        '''
        #def MethodFileCreator(measurement,inputPeakNumber,peaks,csvOutputOn):
        f = open("method.txt","w")

        peaks = self.peaks

        f.write("peakNumber={0}\n".format(len(peaks)))

        '''f.write(chemicalFormulaString + "=")
        for thisPeak in peaks:
            f.write("{0},".format(thisPeak.chemicalFormula))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")'''

        f.write(massString + "=")
        for thisPeak in peaks:
            f.write("{:.6f},".format(thisPeak.mass))
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
        for thisIsotope in peaks.isotopeList:
            f.write("{0},".format(thisIsotope.unit))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")    

        for thisIsotope in peaks.isotopeList:
            f.write("{0},".format(thisIsotope.unit))
        else:
            f.truncate(f.tell()-1)
            f.write("\n")  
        f.write("elutionCurveOn={0}\n".format(peaks.elutionCurveOn))
        f.write("weightedAvgOn={0}\n".format(peaks.weightedAvgOn))
        

        '''f.write("measurementType={0}\n".format(measurement))
        f.write("polarityMode={0}\n".format(polarity))
        if measurement == 'GC-reservoir':
            f.write("minIntensity={0}\n".format(cullingCriteria.minIntensity))
        elif measurement == 'ESI-syringe pump':
            f.write("startTime={0}\n".format(cullingCriteria.startTime))
            f.write("stopTime={0}\n".format(cullingCriteria.stopTime))
        elif measurement == 'GC direct elution':
            f.write("arrivalTime={0}\n".format(cullingCriteria.arrivalTime))
            f.write("exitTime={0}\n".format(cullingCriteria.exitTime))    
        elif measurement == 'small sample':
            f.write("minIntrTIC={0}\n".format(cullingCriteria.minIntrTIC))'''
        if peaks.csvOutputOn != False:
            f.write("csvFileChoice={0}\n".format(peaks.csvOutputPath))
    
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


