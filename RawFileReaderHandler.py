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

def ProcessRawFile(methodFilePath, filePath, outputPath):
    '''
    Handle the call the C# .exe to process .RAW files into JSON that the data processing software can handle
    '''
    args = [] #methodFilePath, fileOrFolderPath, outputPath

    #call .exe and pass in method to process the raw file to JSON

    #command = ".exe" 
    command = r'/Users/sarahzeichner/Documents/Caltech/Research/Code/Orbitrap Data Processing Script/SG-Statistic/SG-Statistic/bin/Debug/SG-Statistic.exe'
    output = check_output(command)
    
    return output

def ReadJsonRawFileAsDataFrame(fileName):
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

def CalculateTICITProduct(dfList):
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
        df['TICxIT'] = df['TICList'] * df['ITList']
        dfListRev = dfList
    return dfListRev            

def ExportDataFrameToCSV(fileName, dfList): 
    '''
    Function to output dataframe to CSV if user wants that option

    fileNameExport = fileName + '_culled.csv'
    export = open(fileNameExport, 'wb')
    wrt = csv.writer(export, dialect = 'excel')
    export.close()
    '''
    fileName = fileName.rsplit( ".", 1 )[ 0 ] 
    for peak in range(len(dfList)):
        pk = str(peak)
        dfList[peak].to_csv(fileName + 'peak' + pk + '_original.csv')
    return

fileName = "/Users/sarahzeichner/Documents/Caltech/Research/Code/Orbitrap Data Processing Script/tester files/20200205_2_USGS37_full1.RAWoutput.txt"
df = ReadJsonRawFileAsDataFrame(fileName)
print(df)