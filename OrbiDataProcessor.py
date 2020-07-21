##!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Modified: Monday July 20, 2020

@author: sarahzeichner

This is the main GUI for data analysis, that emcompasses functions for data analysis
"""
#Import general libraries

from tkinter import *
from tkinter import filedialog 
import os
import time  
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler  
from functools  import partial

#Import libraries for different data analysis
import DataAnalyzer
import MethodFile
import Peak

class Watchdog(PatternMatchingEventHandler, Observer):
    '''
    This class watches a specific path for changes, and processes raw files as they are added or deleted to the path.

    '''
    def __init__(self, path='.', patterns='*', logfunc=print):
        '''
        Instantiate the watchdog object
        '''
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)
        self.schedule(self, path=path, recursive=False)
        self.log = logfunc

    def on_created(self, event):
        '''
        Action upon creation/addition of new file to the folder
        '''
        
        #TODO: fix logic for watchdog
        #ProcessRawFile()
        #self.analyze_folder()

        self.log(f"RAW File added and processed: {event.src_path}")

    def on_deleted(self, event):
        '''
        Action upon deletion of a file to the folder
        '''
        #self.analyze_folder()

        self.log(f"Raw file deleted: {event.src_path}!")

class GUI:
    '''
    GUI for RAW file data processing and analysis
    '''
    def __init__(self):
        '''
        Instantiate the GUI
        '''
        self.folderName = '.'
        self.methodFile = []
        self.numPeaks = 0
        self.peaks = []
        self.watchdog = None
        self.window = Tk()
        self.autoWatchOn = 0
        self.messagebox = Text(width=80, height=10)
        self.messagebox.grid(row=6)

        self.window.title("Welcome to the data processor")
        methodButton = Button(self.window, text="Create a method file", command=self.build_method_file)
        methodButton.grid(row=0, column=0)
        dataFolderButton = Button(self.window, text='Choose data folder directory', command=self.set_local_directory_Folder)
        dataFolderButton.grid(row=1, column=0)
        self.autoWatchOn = IntVar()
        autoWatchOnCheckbutton = Checkbutton(self.window, text='Automatically watch folder?', variable =self.autoWatchOn, onvalue=1, offvalue=0, command=self.automatically_Watch_Files_On)
        autoWatchOnCheckbutton.grid(row=1, column=1)
        rawFileButton = Button(self.window, text='Analyze a raw file', command=self.analyze_File)
        rawFileButton.grid(row=2, column=0)
        rawFolderButton = Button(self.window, text='Process a folder of RAW files', command=self.analyze_Folder)
        rawFolderButton.grid(row=3, column=0)

        #TODO: add styling to the GUI
        self.window.mainloop()

    def log(self, message):
        '''
        Log alerts to the GUI
        '''
        self.messagebox.insert(END, f'{message}\n')
        self.messagebox.see(END)

    def set_local_directory_Folder(self):
        '''
        Folder browser to select the local directory
        '''
        self.folderName = filedialog.askdirectory(initialdir="/", title = "select a directory")
        self.log('Directory set:' + self.folderName)

    def analyze_File(self):
        '''
        Analyze one specific raw file
        '''
        if self.folderName != "":
            pass
        else:
            self.log('Choose a working directory')
            self.set_local_directory_Folder()
        fileName = filedialog.askopenfilename(initialdir = self.folderName,title = "Select RAW file to analyze",filetypes = (("RAW files","*.RAW"),("all files","*.*")))
        
        if self.methodFile != []:
            #TODO: AnalyzeFile()
            self.log('Raw file processed:' + fileName)
        else:
            self.log("Please create a method file")
            self.build_method_file()

    def analyze_Folder(self):
        '''
        Analyze all the raw files in the local directory
        '''
        if self.folderName != "":
            pass
        else:
            self.log('Choose a working directory')
            self.set_local_directory_Folder()

        if self.methodFile != []:
            #args = get_method_file_properties()
            #DataAnalyzer._calcFolderOutput(inputStandardFolder, cullOn=None, cullZeroScansOn=False, gcElutionOn=gc_elution_on, weightByNLHeight=False, gcElutionTimes = peakTimeFrames,  cullAmount=2, isotopeList = isotopeList, NL_over_TIC=0.10, omitRatios = omitRatios, fileCsvOutputPath=None)
            self.log('Folder processed:' + self.folderName)
        else:
            self.log("Please create a method file before you analyze a folder of raw files")
            self.build_method_file()

    def build_method_file(self):
        '''
        Toplevel window to build a method file based on a specified number of peaks
        '''
        def exit_button():
            '''
            Exit out of top level
            '''
            topLevel.destroy()
            topLevel.update()

        self.methodFile = [] 
        topLevel = Toplevel(self.window)
        l = Label(topLevel, text="Create Method File")
        l.grid(row=0)

        Label(topLevel, text="Add number of peaks").grid(row=1, column = 0)
        peaksVar = StringVar()
        peakLabelEntry = Entry(topLevel, textvariable=peaksVar)
        peakLabelEntry.grid(row=1, column = 1)
        submitButton = Button(topLevel, text="SUBMIT", command= lambda *args:self.get_methodFile_input(peaksVar))
        submitButton.grid(row=2, column=0)

        exit_button = Button(topLevel, text="EXIT", command=exit_button)
        exit_button.grid(row=3, column = 0)

    def get_methodFile_input(self, peaksVar):
        '''
        Top level window to take in method file input and create new method file
        '''
        def exit_button():
            '''
            Exit out of top level 
            '''
            topLevel.destroy()
            topLevel.update()

        topLevel = Toplevel(self.window)
        numPeaks= int(peaksVar.get())

        Label(topLevel, text="Mass").grid(row=0, column=0)
        Label(topLevel, text="Tolerance").grid(row=0, column=1)
        Label(topLevel, text="ToleranceUnits").grid(row=0, column=2)

        massVar = {}
        toleranceVar = {}
        toleranceUnitsVar = {}

        for peak in range(numPeaks):      
            massVar["string{0}".format(peak)] = StringVar()
            mass = Entry(topLevel, textvariable=massVar["string{0}".format(peak)])
            mass.grid(row=peak+1, column=0)
            
            toleranceVar["string{0}".format(peak)] = StringVar()
            tolerance = Entry(topLevel, textvariable=toleranceVar["string{0}".format(peak)])
            tolerance.grid(row=peak+1, column=1)
            
            toleranceUnitsVar["string{0}".format(peak)] = StringVar()
            toleranceUnits = Entry(topLevel, textvariable=toleranceUnitsVar["string{0}".format(peak)])
            toleranceUnits.grid(row=peak+1, column=2)

        lastRowNum = numPeaks+3

        Label(topLevel, text="IsotopeList (e.g., ['UnSub','15N','13C'])").grid(row=lastRowNum, column=0)
        isotopeListVar = StringVar()
        isotopeList = Entry(topLevel, textvariable=isotopeListVar)
        isotopeList.grid(row=lastRowNum, column=1)

        Label(topLevel, text="ElutionCurveOn (True/False)").grid(row=lastRowNum+1, column=0)
        elutionCurveToggleVar = StringVar()
        elutionCurveToggle = Entry(topLevel, textvariable=elutionCurveToggleVar)
        elutionCurveToggle.grid(row=lastRowNum+1, column=1)

        Label(topLevel, text="WeightedAvgOn (True/False)").grid(row=lastRowNum+2, column=0)
        weightAvgToggleVar = StringVar()
        weightAvgToggle = Entry(topLevel, textvariable=weightAvgToggleVar)
        weightAvgToggle.grid(row=lastRowNum+2, column=1)

        Label(topLevel, text="CSVOutputOn (True/False)").grid(row=lastRowNum+3, column=0)
        csvOutputToggleVar = StringVar()
        csvOutputToggle = Entry(topLevel, textvariable=csvOutputToggleVar)
        csvOutputToggle.grid(row=lastRowNum+3, column=1)

        Label(topLevel, text="CSVOutputPath").grid(row=lastRowNum+4, column=0)
        csvOutputPathVar = StringVar()
        csvOutputPath = Entry(topLevel, textvariable=csvOutputPathVar)ya
        csvOutputPath.grid(row=lastRowNum+4, column=1)

        submitButton = Button(topLevel, text="SUBMIT", command= lambda *args:self.submit_method_file(numPeaks, massVar, toleranceVar, toleranceUnitsVar, isotopeListVar, weightAvgToggleVar, elutionCurveToggleVar, csvOutputToggleVar, csvOutputPathVar))
        submitButton.grid(row=lastRowNum+5, column = 2)

        exit_button = Button(topLevel, text="EXIT", command=exit_button)
        exit_button.grid(row=lastRowNum+6, column = 2)

    def submit_method_file(self, numPeaks, massVar, toleranceVar, toleranceUnitsVar, isotopeListVar, weightAvgToggleVar, elutionCurveToggleVar, csvOutputToggleVar, csvOutputPathVar):
        '''
        Take method file input within toplevel widget and create a method file output that is written to local directory and can be used for future data analysis
        '''

        for peak in range(numPeaks):      
            thisMass = massVar["string{0}".format(peak)].get()
            thisTol = toleranceVar["string{0}".format(peak)].get()
            thisTolUnits = toleranceUnitsVar["string{0}".format(peak)].get()
            self.peaks.append(Peak.Peak(thisMass, thisTol, thisTolUnits))
            
        thisIsotopeList = isotopeListVar.get()
        thisElutionCurveToggle= elutionCurveToggleVar.get()
        thisWeightAvgToggle = weightAvgToggleVar.get()
        thisCsvOutputToggle = csvOutputToggleVar.get()
        thisCsvOutputPath = csvOutputPathVar.get()

        self.MethodFile = MethodFile.MethodFile(inputPeaks=self.peaks, isotopeList=thisIsotopeList, elutionCurveOn=thisElutionCurveToggle, weightedAvgOn=thisWeightAvgToggle, csvOutputOn=thisCsvOutputToggle, csvOutputPath=thisCsvOutputPath)
        self.MethodFile.WriteMethodFile()
        self.log("Method File created at location:" + str(os.curdir) + "/method.txt")

    def automatically_Watch_Files_On(self):
        '''
        Logic to monitor the watchdog toggle
        '''
        autoWatchToggle = self.autoWatchOn.get()
        if autoWatchToggle == 0:
            self.stop_watchdog()
        elif autoWatchToggle ==1:
            self.start_watchdog()

    def start_watchdog(self):
        '''
        Start the watchdog on local directory when the checkbox is clicked
        '''
        if self.watchdog is None:
            self.watchdog = Watchdog(path=self.folderName, logfunc=self.log)
            self.watchdog.start()
            self.log('Watchdog started')
        else:
            self.log('Watchdog already started')

    def stop_watchdog(self):
        '''
        Stop the watchdog on local directory when the checkbox is un-clicked
        '''
        if self.watchdog:
            self.watchdog.stop()
            self.watchdog = None
            self.log('Watchdog stopped')
        else:
            self.log('Watchdog is not running')


if __name__ == '__main__':
    GUI()
