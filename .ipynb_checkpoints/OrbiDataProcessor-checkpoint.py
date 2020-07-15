##!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Modified: Wed July 15, 2020

@author: sarahzeichner
"""
from tkinter import *
from tkinter import filedialog 
   
# Function for opening the  
# file explorer window 
def browseFiles(): 
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("Text files", 
                                                        "*.txt*"), 
                                                       ("all files", 
                                                        "*.*"))) 
       
    # Change label contents 
    label_file_explorer.configure(text="File Opened: "+filename) 
       
       
                                                                                                   
# Create the root window 
window = Tk() 
   
# Set window title 
window.title('File Explorer') 
   
# Set window size 
window.geometry("500x500") 
   
#Set window background color 
window.config(background = "white") 
   
# Create a File Explorer label 
label_file_explorer = Label(window,  
                            text = "File Explorer using Tkinter", 
                            width = 100, height = 4,  
                            fg = "blue") 
   
       
button_explore = Button(window,  
                        text = "Browse Files", 
                        command = browseFiles)  
   
button_exit = Button(window,  
                     text = "Exit", 
                     command = exit)  
   
# Grid method is chosen for placing 
# the widgets at respective positions  
# in a table like structure by 
# specifying rows and columns 
label_file_explorer.grid(column = 1, row = 1) 
   
button_explore.grid(column = 1, row = 2) 
   
button_exit.grid(column = 1,row = 3) 
   
# Let the window wait for any events 
window.mainloop() 

#Select a folder for analysis

#Look for a method file
#if !exists, call method file creator

#while loop (folder watch for new file)
    #if new file, process raw file into json


#choose files, and analyze 