##!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Modified: Tuesday July 21, 2020

@author: sarahzeichner, elisewilkes, timcsernica

This file handles the calls to the RAW File Reader code .exe, which processes data to be used downstream by analysis software
"""

from subprocess import check_output
import json
import pandas as pd
import numpy as np

def ProcessRawFile(methodFilePath, fileOrFolderPath, outputPath):
    '''
    Handle the call the C# .exe to process .RAW files into JSON that the data processing software can handle
    '''
    args = [] #methodFilePath, fileOrFolderPath, outputPath

    #call .exe and pass in method to process the raw file to JSON

    #command = ".exe" 
    command = r'/Users/sarahzeichner/Documents/Caltech/Research/Code/Orbitrap Data Processing Script/SG-Statistic/SG-Statistic/bin/Debug/SG-Statistic.exe'
    output = check_output(command)
    
    return output

def readFile(fileName):
    '''
    Borrowed and modified from Tim's readAndRejectJSON.py script
    Takes a JSON output file from the .RAW file reader and turns it into a list of dataFrames. There is one dataFrame for each peak extracted from 
    the .RAW file. For now, parameter IT must be added manually as a stand-in for real data. 
    Inputs:
        fileName: A string specifying the path of the file to read in
        
    Outputs:
        dfList: A list of dataframes, with one dataframe for each peak. 
    '''
    with open(fileName) as f:
        data = json.load(f)
        
        dfList = []
        for peak in data:
            df = pd.DataFrame.from_dict(peak)
            dfList.append(df)
            
            for df in dfList:
                df['IT'] = 1 #temporary; no IT parameter in SG-Statistic output
                
    return dfList          

def productTicIt(dfList):
    '''
    Takes a dataframe of outputs from SG-Statistic and adds a new column
    containing the product TICxIT
    Inputs:
        dfList: A list of dataframes, with one dataframe for each peak
    Outputs:
        dfListRev: A list of revised dataframes (each containing a new column 
        for TICxIT). 
    '''
    
    for df in dfList:
        df['TICxIT'] = df['SpectraTIC'] * df['IT']
        dfListRev = dfList
    return dfListRev            

def calcStatsTicIt(dfListRev):
    '''
    For each peak: calculates statistics on all scans of the product TICxIT
    Inputs:
        dfListRev: A list of dataframes, with one dataframe for each peak, and containing a column for TICxIT
        
    Outputs:
        (mean, median, std): vectors containing the mean TICxIT, median TICxIT, and standard deviation of TICxIT for each peak. 
    '''
    median = np.zeros(len(dfListRev)) #create empty arrays to populate
    mean = np.zeros(len(dfListRev))
    std = np.zeros(len(dfListRev))
    
    for peak in range(len(dfListRev)):
        median[peak] = dfListRev[peak]['TICxIT'].median() #not currently used, but may be useful for future culling decisions
        mean[peak] = dfListRev[peak]['TICxIT'].mean()
        std[peak] = dfListRev[peak]['TICxIT'].std()
    return (median, mean, std)

def cullTicIt(mean, std, stdThreshold, dfListRev):
    '''
    Culls scans falling outside a specified number of standard deviations of the mean TICxIT.
    Inputs:
        mean: a vector containing the mean TICxIT for each peak
        std: a vector containing the standard deviation of TICxIT for each peak
        stdThreshold: a multiplier (float) specifying how many standard deviations from the mean should be included in the final culled dataset
        dfListRev: A list of dataframes, with one dataframe for each peak, containing an added column for TICxIT
        
    Outputs:
        dfCulled: A list of culled dataframes, with one dataframe for each peak.
        Scans falling outside, e.g., 1 SD of the mean TICxIT have been removed.
    '''  
    dfCulled = []
    
    for peak in range(len(dfListRev)):
        df = dfListRev[peak]
        df = df[(df.TICxIT < mean[peak] + (stdThreshold * std[peak])) & 
                (df.TICxIT > mean[peak] - (stdThreshold * std[peak]))] 
        dfCulled.append(df)
        
    return dfCulled

def dataExporter(fileName, dfCulled, dfList): #optional, in case we choose to output .csv files after culling for user records
    '''
    fileNameExport = fileName + '_culled.csv'
    export = open(fileNameExport, 'wb')
    wrt = csv.writer(export, dialect = 'excel')
    export.close()
    '''
    fileName = fileName.rsplit( ".", 1 )[ 0 ] 
    for peak in range(len(dfCulled)):
        pk = str(peak)
        dfCulled[peak].to_csv(fileName + 'peak' + pk + '_culled.csv')
    for peak in range(len(dfList)):
        pk = str(peak)
        dfList[peak].to_csv(fileName + 'peak' + pk + '_original.csv')
    return