##!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Modified: Thurs July 16, 2020

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
import Peak

class Watchdog(PatternMatchingEventHandler, Observer):
    def __init__(self, path='.', patterns='*', logfunc=print):
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)
        self.schedule(self, path=path, recursive=False)
        self.log = logfunc

    def on_created(self, event):

        #TODO: fix logic for watchdog
        #ProcessRawFile()
        #AnalyzeFolder()
    
        self.log(f"RAW File added and processed: {event.src_path}")

    def on_deleted(self, event):

        # AnalyzeFolder()

        self.log(f"Raw file deleted: {event.src_path}!")

class GUI:
    def __init__(self):
        self.folderName = '.'
        self.methodFile = []
        self.numPeaks = 0
        self.peaks = []
        self.watchdog = None
        self.window = Tk()
        self.autoWatchOn = 0
        self.messagebox = Text(width=80, height=10)
        self.messagebox.grid(row=6)

        #frm = Frame(self.window)
        self.window.title("Welcome to the data processor")
        methodButton = Button(self.window, text="Create a method file", command=self.build_method_file)
        methodButton.grid(row=0, column=0)
        dataFolderButton = Button(self.window, text='Choose data folder directory', command=self.browse_Folders)
        dataFolderButton.grid(row=1, column=0)
        self.autoWatchOn = Checkbutton(self.window, text='Automatically watch folder?', onvalue=1, offvalue=0, command=self.automatically_Watch_Files_On)
        self.autoWatchOn.grid(row=1, column=1)
        rawFileButton = Button(self.window, text='Analyze a raw file', command=self.analyze_File)
        rawFileButton.grid(row=2, column=0)
        rawFolderButton = Button(self.window, text='Process a folder of RAW files', command=self.analyze_Folder)
        rawFolderButton.grid(row=3, column=0)

        #TODO: add styling to the GUI
        self.window.mainloop()

    def start_watchdog(self):
        if self.watchdog is None:
            self.watchdog = Watchdog(path=self.folderName, logfunc=self.log)
            self.watchdog.start()
            self.log('Watchdog started')
        else:
            self.log('Watchdog already started')

    def stop_watchdog(self):
        if self.watchdog:
            self.watchdog.stop()
            self.watchdog = None
            self.log('Watchdog stopped')
        else:
            self.log('Watchdog is not running')

    def log(self, message):
        self.messagebox.insert(END, f'{message}\n')
        self.messagebox.see(END)

    def browse_Folders(self):
        self.folderName = filedialog.askdirectory(initialdir="/", title = "select a directory")
        self.log('Directory set:' + self.folderName)

    def analyze_File(self):
        if self.folderName != "":
            pass
        else:
            self.log('Choose a working directory')
            self.browse_Folders()
        fileName = filedialog.askopenfilename(initialdir = self.folderName,title = "Select RAW file to analyze",filetypes = (("RAW files","*.RAW"),("all files","*.*")))
        
        if self.methodFile != []:
            #TODO: analyze file
            self.log('Raw file processed:' + fileName)
        else:
            self.log("Please create a method file")
            self.build_method_file()

    def analyze_Folder(self):
        if self.folderName != "":
            pass
        else:
            self.log('Choose a working directory')
            self.browse_Folders()

        if self.methodFile != []:
            #TODO: analyze folder
            self.log('Folder processed:' + self.folderName)
        else:
            self.log("Please create a method file before you analyze a folder of raw files")
            self.build_method_file()

    def build_method_file(self):

        self.methodFile = [] 
        topLevel = Toplevel(self.window)
        l = Label(topLevel, text="Create Method File")
        l.grid(row=0)

        def exit_top():
            topLevel.destroy()
            topLevel.update()

        def submit_method():
            topLevel.destroy()
            self.get_peak_input()

        Label(topLevel, text="Add number of peaks").grid(row=1, column = 0)
        peakLabelEntry = Entry(topLevel)
        peakLabelEntry.grid(row=1, column = 1)
        self.numPeaks = peakLabelEntry.get()
        submitButton = Button(topLevel, text="Submit", command=submit_method)
        submitButton.grid(row=2, column=0)

        ''''if self.numPeaks != 0:
            self.get_peak_input(topLevel, self.numPeaks)'''

        #Button(topLevel, text="Add another peak", command=self.get_peak_input(topLevel)).grid(row=0)
        #Button(topLevel, text="Specify run information", command=self.specify_run_information).grid(row=1)
        #Button(topLevel, text="Finish method file creation", command=self.generate_method_file).grid(row=2, column=0)
        #Button(topLevel, text="Quit method creation", command=exit_top).grid(row=2, column =1)

    def generate_method_file(self):
        #MethodFile()
        self.log("Method file created at location:")

    def get_peak_input(self):
        topLevel = Toplevel(self.window)
        l = Label(topLevel, text="Create Method File")
        l.grid(row=0)

        for peak in self.numPeaks:      
            continue

        Label(t ,text = "Mass").grid(row=0, column = 0)
        a = Entry(t)
        a.grid(row=0, column = 2)
        mass = a.get()

        Label(t ,text = "Tolerance").grid(row=0, column=1)
        b = Entry(t)
        b.grid(row=1, column=2)
        tol = b.get()
        
        Label(t ,text = "Tolerance units").grid(row=0, column=2)
        c = Entry(t)
        c.grid(row=2, column=2)
        tolunits = c.get()

        peak = [mass, tol, tolunits]
        self.peaks.append(peak)
        self.log("Peak  added:" + str(mass))

    def specify_run_information(self):
        
        runInfo = []
        #isotope list
        #elutionCurveOn
        #weightedAvgOn
        #csvOutputOn
        #csvOutputPath
        self.log("Run information  updated." )
        return runInfo


    def automatically_Watch_Files_On(self):
        if self.autoWatchOn == 0:
            self.stop_watchdog()
        elif self.autoWatchOn ==1:
            self.start_watchdog()

if __name__ == '__main__':
    GUI()
