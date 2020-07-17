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
        self.watchdog = None
        self.window = Tk()
        self.autoWatchOn = 0
        self.messagebox = Text(width=80, height=10)
        self.messagebox.pack()
        frm = Frame(self.window)

        Button(frm, text="Create a method file", command=self.create_method_file).pack(side=LEFT)
        Button(frm, text='Choose data folder directory', command=self.browse_Folders).pack(side=LEFT)
        self.autoWatchOn = Checkbutton(self.window, text='Automatically watch folder?', onvalue=1, offvalue=0, command=self.automatically_Watch_Files_On)
        self.autoWatchOn.pack()
        Button(frm, text='Analyze a raw file', command=self.analyze_File).pack(side=LEFT)
        Button(frm, text='Process a folder of RAW files', command=self.analyze_Folder).pack(side=LEFT)

        #TODO: add styling to the GUI

        frm.pack(fill=X, expand=1)
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
            self.create_method_file()

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
            self.create_method_file()

    def create_method_file(self):
        self.methodFile = [] 

        #TODO: create method file widget subwindow
        #create fillable form for method file
        #create a child window
        #prompt for number of peaks
        #populate peak objects with input peaks
        #
        #MethodFile.WriteMethodFile()

        self.log('Method file created')

    def automatically_Watch_Files_On(self):
        if self.autoWatchOn == 0:
            self.stop_watchdog()
        elif self.autoWatchOn ==1:
            self.start_watchdog()

if __name__ == '__main__':
    GUI()