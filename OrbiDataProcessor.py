##!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Modified: Wed July 15, 2020

@author: sarahzeichner
"""
#Import general libraries
from tkinter import *
from tkinter import filedialog 
import os
import time  
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler  

#Import libraries for different data analysis
import DataAnalyzer
import MethodFile

#Global variables
folderName = ""
methodPath = ""
methodFile = []

# Function for opening the file explorer window 
def browseFiles(): 
    '''
    Browse files on the local computer
    '''
    if folderName:
        directory = folderName
    else:
        directory = "/"
    fileName = filedialog.askopenfilename(initialdir = directory, 
                                          title = "Select a File", 
                                          filetypes = (("Raw files", 
                                                        "*.RAW"), 
                                                       ("all files", 
                                                        "*.*"))) 
       
    # Change label contents 
    fileExplorerLabel.configure(text="File Opened: " +fileName) 

def browseFolders():
    '''
    Browse folders and set global variable for the local directory
    '''
    folderName = filedialog.askdirectory(initialdir="/",
                                         title = "select a directory")
    folderExploreLabel.configure("Folder opened:" +folderName)

def createMethodFile():
    #create fillable form for method file
    #create a child window
    #prompt for number of peaks
    #populate peak objects with input peaks
    #
    methodPath = ""
    
    #populate methodFile object

    methodFileLabel.configure("MethodFile:" + methodPath)
    return 


def getSetMethodFile(methodPath):
    '''
    Get method file in the local directory, and create a MethodFile object to
    process the data.
    '''
    if os.path.exists(methodPath):
        #methodFile = MethodFile(methodPath) #TODO: get method file object, and return it
        pass
    else:
        print("Please create a method file") #make sure that this 
        methodFile = []
    return methodFile
    #TODO: get method file
    #if it doesn't exist, prompt to create one

#def processDataFolder(folderName):

def printUpdate(printText):
    '''
    Print something everything a file is processed

    Input: text to print
    '''
    label = Label(window, text= printText)
    label.pack() 
    
# Create the root window 
window = Tk() 
window.title('Orbitrap Data Analyzer') 
window.geometry("500x500") 
window.config(background = "white") 
   
# Create a method file
methodFileLabel = Label(window, text = "Create a method file")    
methodFileLabel.pack()
methodFileCreationButton = Button(window,text = "Create", command = createMethodFile)  
methodFileCreationButton.pack()

# Set data directory and properties for data analysis
folderExploreLabel = Label(window, text = "Set the data directory")    
folderExploreLabel.pack()
folderExploreButton = Button(window,text = "Browse Folders", command = browseFolders)  
folderExploreButton.pack()
automaticallyWatchFilesOn = Checkbutton(window, text='Automatically watch folder?', onvalue=1, offvalue=0)
automaticallyWatchFilesOn.pack()  

# Choose raw file for specific analysis
fileExplorerLabel = Label(window, text = "Choose RAW file for analysis")
fileExplorerLabel.pack()
fileExploreButton = Button(window, text = "Browse Files", command = browseFiles)  
fileExploreButton.pack()    

#Window to print processed data
   
exitButton = Button(window,text = "Exit",command = exit)  
exitButton.pack()

#TODO: add formatting for window 

# Let the window wait for any events 
window.mainloop() 

#Look for a method file, and call method file creator if it doesn't exist
if folderName != "":
    methodFile = getSetMethodFile(folderName)

#Process raw files for automatic file watcher
if methodFile != [] and automaticallyWatchFilesOn==1:
    #Watchdog: WatchDirectoryForRawFiles()
    #Check for methodFile, otherwise prompt to create
    #watchdog: WatchDirectoryForJson()
    #RawFileProcessor.ProcessRawFile.exe(methodFile, rawFileName)
    #processFile()
    #calculateSummaryStatistics()

    printUpdate("RAW File Processed: [fileName], with output")
    pass

#Process a folder of data upon request
#if processDataFolder!=""
    #rpocessDataFolder()
    #calculateSummaryStatistics()

#Process a single file, with data visualizations
#if processSingleFile!=""
    #processDataFile()
    #if visualizeData==1:
        #visualizeData()

#TODO: publish errors to window