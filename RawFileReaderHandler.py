##!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Modified: Monday July 20, 2020

@author: sarahzeichner

This file handles the calls to the RAW File Reader code .exe, which processes data to be used downstream by analysis software
"""

from subprocess import check_output

def ProcessFileOrFolder(methodFilePath, fileOrFolderPath, outputPath):
    '''
    Handle the call the C# .exe to process .RAW files into JSON that the data processing software can handle
    '''
    args = [] #methodFilePath, fileOrFolderPath, outputPath

    #call .exe and pass in method to process the raw file to JSON

    #command = ".exe" 
    command = r'.exe'
    output = check_output(command)
    
    return output



