##!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Modified: Wed July 15, 2020

@author: sarahzeichner
"""
from tkinter import *
from tkinter import filedialog 
import os
import time  
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler  
import DataAnalyzer

folderName = ""
methodPath = ""
methodFile = []

# Function for opening the  
# file explorer window 
def browseFiles(): 
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
    folderName = filedialog.askdirectory(initialdir="/",
                                         title = "select a directory")
    folderExploreLabel.configure("Folder opened:" +folderName)

def getSetMethodFile(methodPath):
    methodFile = [] #TODO: get method file object, and return it
    return methodFile
    #TODO: get method file
    #if it doesn't exist, prompt to create one

#def processDataFolder(folderName):
    
    
# Create the root window 
window = Tk() 
window.title('Orbitrap Data Analyzer') 
window.geometry("500x500") 
window.config(background = "white") 
   
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