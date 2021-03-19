import os
import sys
import shutil, sys  
import pytesseract
from pytesseract import Output
from PIL import Image
import subprocess
from fpdf import FPDF 
from subprocess import  Popen
from cv2 import cv2
import PyPDF2
from xlrd import open_workbook
import csv
import datetime 
import nltk
from nltk.corpus import stopwords
from docx import Document
from nameparser.parser import HumanName
import re
import operator
import time
import textract
import img2pdf
import pdfkit
import os.path, time
import datefinder
import sqlite3
from sqlite3 import Error
import pandas as pd
import datetime
from nltk.tokenize import RegexpTokenizer

from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore
import numpy as np 
from tkinter import *
from tkcalendar import*
import tkinter as tk
from tkinter import filedialog
import getpass
from tkinter import messagebox 
from tkinter import simpledialog 
# from HyperlinkManager import *
from tkinter import ttk
import webbrowser

#user files
from doc_functions import *
from watermark import *
from Tkinter_window import *
# from Drive.py import *

strfil = ''
filepath = ''
todateselected = ''
fromdateselected = ''
x = 0
y = 0
w = 0
h = 0
usertags = ''
newfile = ''

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
##########################     Files Found Copy-able text dialog   ##########################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class CustomDialog(simpledialog.Dialog):

    def __init__(self, parent, title=None, text=None):
        self.data = text
        simpledialog.Dialog.__init__(self, parent, title=title)

    def body(self, parent):

        self.text = tk.Text(self, width=100, height=15)
        self.text.pack(fill="both", expand=True)
        self.text.insert("1.0", self.data)

        return self.text

def show_dialog(matches):
    
    class Checkbar(Frame):
        def __init__(self, parent, pick=[], side=LEFT, anchor=W):
            Frame.__init__(self, parent)
            i=0
            self.vars = []
            self.filenames = []
            # for pick in picks:
            var = IntVar(top)              
            chk = Checkbutton(self, text="", variable=var).grid(row=0,column = 0)
            self.vars.append(var)
            self.filenames.append(pick)
                
    def state(cls):
            bool_var = map((lambda var: var.get()), cls.vars)
            from itertools import compress
            final_list = list(compress(cls.filenames,bool_var))
            return final_list

    def watermarkandcopy(pdffile):
        global watertxt
        watermarktxt = watertxt.get(1.0,"end")
        # print(pdfmatches)
        for pdff in pdffile:
            apply_watermark(watermarktxt,pdff)

    def callback(url,state_copytodesktop):
      global var,var1,var2
      pdffile = matches.loc[matches['original_file'] == url,'pdf_file']
      if var2.get() ==1:
          webbrowser.open_new(url)
      if var1.get() ==1:
          watermarkandcopy(pdffile)
      if state_copytodesktop:
          copytodesktop(url)

    def copytodesktop(files_selected): 
      filename = os.path.basename(files_selected)  #original File name
      os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
      originalfilepath =os.path.expanduser("~/Desktop")+ '/'+ filename
      from shutil import copyfile
      copyfile(files_selected, originalfilepath)
      print("Files Copied")

    def watermark():        
        global watertxt
        left = Label(bottom, text="Enter watermark text", font = "Calibri 10 italic")
        left.grid(row = 3,column= 0)
        
        watertxt=Text(bottom,width=30,height=2)
        watertxt.insert(tk.END, "Confidential")
        watertxt.grid(row = 3,column= 1)
        

    master = Tk()
    master.title("Files Found")
    master.geometry("600x400")

    top = Frame(master)
    bottom = Frame(master)
    # top.pack(side=TOP)
    # bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
    top.grid(row = 0,column =0)
    bottom.grid(row = 1,column =0)
    eval_link = lambda x: (lambda p: callback(x,var.get()))

    unique_matches = list(dict.fromkeys(matches['original_file'].tolist()))
    unique_pdf_matches = list(dict.fromkeys(matches['pdf_file'].tolist()))

    global var,var1,var2
    i=0
    for pick in unique_matches:
      i = i+1
      link = Label(top, text=os.path.basename(pick), fg="blue", cursor="hand2")
    #   checkfile = Checkbar(top, matches)
    #   checkfile.grid(row=i,column = 0)
      link.grid(row=i,column = 1)
      link.bind("<Button-1>", eval_link(pick))

    var = IntVar(bottom)
    chk = Checkbutton(bottom, text='Copy to desktop', variable=var)
    chk.grid(row = 0,column=0)
    
    watermark()
    var1 = IntVar(bottom)
    chk1 = Checkbutton(bottom, text='Download Watermarked pdf to desktop', variable=var1)
    chk1.grid(row = 1,column=0)

    watermark()
    var2 = IntVar(bottom)
    chk2 = Checkbutton(bottom, text='Open File', variable=var2)
    chk2.grid(row = 2,column=0)

    # my_button2=Button(bottom,text="Download Watermarked pdf to desktop ", command=watermark)
    # my_button2.grid(row = 1,column=0)

    master.mainloop()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
##########################     Files Upload from Front End         ##########################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def UploadFile():
    global w,h,x,y,x1upload ,y1upload ,w1upload ,h1upload,frame1,frame3
  
    def saveusertags():
        global usertags
        usertags=my_text3.get(1.0,"end")
        print(usertags)

    def openfiledialog():
        global strfil,filepath,file_str
        print("Hello User")
        root=tk.Tk()
        root.withdraw()
        files=filedialog.askopenfilenames(parent=root)
        files = root.tk.splitlist(files)
        aList = list(files)
        filelist = [os.path.basename(i) for i in aList] 
        # print(filelist)
        my_text2.insert(1.0, filelist)
        file_str=aList
        root.lift()

    def cleartextbox():
        global strfil
        my_text2.delete(1.0,"end")
        strfil=''

    def savename():
        newfile=new_filename.get(1.0,"end")
        newfile = newfile.strip('\n')
        print(newfile)
        file_urls = fileUpload(filepathi,usertags,0,1,0,newfile)
        messagebox.showinfo("Message","File uploaded",parent = root)

    def newnamepopup():
        global newfile,new_filename
        filename = os.path.basename(filepathi)
        mas = createwindow("New file name",300,300)
        newfile  = filename.split(".")[0] + "_1"
        left = Label(mas ,text="Enter New File Name", font = "Calibri 10 italic")
        left.grid(row = 0,column=0,sticky='W', padx=5, pady=5,columnspan=2)
        new_filename=Text(mas,width=30,height=2)
        new_filename.grid(row = 1,column=1,sticky='W', padx=5, pady=5,columnspan=2)
        new_filename.insert(1.0,newfile)
        new_file_ok=Button(mas,text="OK", command=savename)
        new_file_ok.grid(row=2,column=1,  padx=5, pady=2, sticky='E')
        return newfile

    def replacefile():
        file_urls = fileUpload(filepathi,usertags,0,0,1,'')
        messagebox.showinfo("Message","File uploaded",parent = root)

    def filexistspopup():
        global newfile,new_filename
        filename = os.path.basename(filepathi)
        mas1 = createwindow("New file name",300,100)
        newfile  = filename.split(".")[0] + "_1"
        left = Label(mas1 ,text="File Name already exists", font = "Calibri 10 italic")
        left.grid(row = 0,column=0,sticky='W', padx=5, pady=5,columnspan=2)

        replace=Button(mas1,text="Replace", command=replacefile)
        replace.grid(row=2,column=1,  padx=5, pady=2, sticky='E')
        Rename=Button(mas1,text="Rename", command=newnamepopup)
        Rename.grid(row=2,column=2,  padx=5, pady=2, sticky='E')

    def UploadFilesFE():
        # filepath  = file_str.split(",")
        filepaths = file_str
        saveusertags()
        for i in range(len(filepaths)):
          global filepathi 
          filepathi = filepaths[i]
          filepaths[i] = filepaths[i].replace('"', "") 
          filename = os.path.basename(filepaths[i])
          print(datetime.datetime.now())
          if fileExists(filepaths[i]):
              filexistspopup()
          else:
              file_urls = fileUpload(filepaths[i],usertags,0,0,0,'')
              messagebox.showinfo("Message","File uploaded",parent = root)

          print(datetime.datetime.now())

    my_text2=Text(frame1,width=30,height=2)
    my_text2.grid(row = 0,column=0,sticky='WE', padx=5, pady=5,columnspan=2)
    my_text2.grid_columnconfigure(0, weight=1)

    my_button=Button(frame1,text="Select To Upload", command=openfiledialog)
    my_button.grid(row=0,column=2, padx=5, pady=2, sticky='E')

    option = StringVar()
    R1 = Radiobutton(frame1, text="Quick Scan", variable=option , value=1)
    R1.grid(row=4,column=0, padx=5, pady=2, sticky='E')
    
    R2 = Radiobutton(frame1, text="Deep Scan", variable=option  , value=2)
    R2.grid(row=4,column=1, padx=5, pady=2, sticky='E')
    
    R1.deselect()
    R2.deselect()
    
    my_button2=Button(frame1,text="Clear", command=cleartextbox)
    my_button2.grid(row=5,column=1,  padx=5, pady=2, sticky='E')
    my_button3=Button(frame1,text="Upload Files", command=UploadFilesFE)
    my_button3.grid(row=5, column=2,padx=5, pady=2, sticky='E')

    left = Label(frame3 ,text="Enter user tags if any (Optional)", font = "Calibri 10 italic")
    left.grid(row = 0,column=0,sticky='W', padx=5, pady=5,columnspan=2)

    my_text3=Text(frame3,width=30,height=2)
    my_text3.grid(row = 1,column=0,sticky='WE', padx=5, pady=5,columnspan=2)
    my_text3.grid_columnconfigure(0, weight=1)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
##########################     Search File by Date   ##########################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def uploadtags():
    left = Label(frame4, text="Client Details*: Heena", font = "Calibri 10 italic")
    left.grid(row = 1,column=0,sticky='W', padx=5, pady=5)

    left = Label(frame4, text="Date Range*: 2019-2020", font = "Calibri 10 italic")
    left.grid(row = 1,column=2,sticky='W', padx=5, pady=5)

def searchdate(framedate):
    global w,h,x,y,x1searchdate,y1searchdate,w1searchdate ,h1searchdate,todateselected,fromdateselected

    def grab_from_date():
      global fromdateselected
      date=cal.get_date()
      date = datetime.datetime.strptime(date, '%m/%d/%y')
      date=date.strftime('%Y-%m-%d')
      fromdateselected = date
      messagebox.showinfo("From date is :",fromdateselected,parent = root)
    #   print(fromdateselected)

    def grab_to_date():
      global todateselected
      date=cal.get_date()
      date = datetime.datetime.strptime(date, '%m/%d/%y')
      date=date.strftime('%Y-%m-%d')
      todateselected = date
      messagebox.showinfo("To date is :",todateselected,parent = root)
    #   print(todateselected)

    def findbydateFE():
      global fromdateselected,todateselected
      dates = []
      if fromdateselected != "":
        dates.append(fromdateselected)
      else:
        messagebox.showinfo("Disclaimer :","Please select To Date",parent = root)

      if todateselected != "":
        dates.append(todateselected)
      else:
        messagebox.showinfo("Disclaimer :","Please select From Date",parent = root)

      matchesbydate =search_by_date(dates)
      show_dialog(matchesbydate)
      print("Matched files")
    #   print(matchesbydate)

    # for widget in frame5.winfo_children():
    #     widget.destroy()
    # frame5.pack_forget()

    for widget in framedate.winfo_children():
        widget.destroy()
    framedate.pack_forget()

    left = Label(framedate, text="Select To and From Dates to Search For File")
    left.grid(row = 0,column=0,sticky='WE', padx=5, pady=5,columnspan=3)

    cal=Calendar(framedate,selectmode="day",year=2020,month=1,day=1)

    cal.grid(row = 1,column=0,sticky='WE',columnspan = 3)
    cal.grid_columnconfigure(0, weight=1)
    
    my_button=Button(framedate,text="From Date", command=grab_from_date)
    my_button.grid(row=2,column=0, padx=5, pady=2, sticky='E')
    # root.lift()
    my_button=Button(framedate,text="To Date", command=grab_to_date)
    my_button.grid(row=2,column=1, padx=5, pady=2, sticky='E')
    my_button=Button(framedate,text="Search By Date", command=findbydateFE)
    my_button.grid(row=2,column=2, padx=5, pady=2, sticky='E')

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
##########################     Search File by Tag   ##########################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def searchtag():
    global tagstr,w,h,x,y,x1searchtag,y1searchtag ,w1searchtag  ,h1searchtag
   
    def cleartextbox():
        global tagstr
        my_text.delete(1.0,"end")
        tagstr=''
        
    def savetag():
        global tagstr
        tagstr=my_text.get(1.0,"end")
        print(tagstr)    
    
    def searchFileTagFE():
        savetag()
        global tagstr
        tagstr = tagstr.strip('\n')
        tags  = tagstr.split(",")
        matches = search_by_tags(tags)
        show_dialog(matches)
        # print(matches)
    
    for widget in frame2.winfo_children():
        widget.destroy()
    for widget in frame5.winfo_children():
        widget.destroy()
    frame2.pack_forget()
    frame5.pack_forget()

    left = Label(frame2, text="Enter a tag/keyword from your file to search the file")
    left.grid(row = 0,column=0,sticky='WE', padx=5, pady=5,columnspan=3)
    my_text=Text(frame2,width=60,height=2)

    my_text.grid(row = 1,column=0,sticky='WE', padx=5, pady=5,columnspan=3)
    my_text.grid_columnconfigure(0, weight=1)

    my_button2=Button(frame2,text="Clear", command=cleartextbox)
    my_button2.grid(row=2,column=0, padx=5, pady=2, sticky='E')

    my_button2=Button(frame2,text="Search", command=searchFileTagFE)
    my_button2.grid(row=2,column=1, padx=5, pady=2, sticky='E')
    # root.mainloop()
    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
##########################     Search File by Name   ##########################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def searchfile():
    global filestr
    global w,h,x,y,x1searchname ,y1searchname ,w1searchname ,h1searchname,frame2

    def cleartextbox():
        global filestr
        my_text.delete(1.0,"end")
        filestr=''
        
    def savetag():
        global filestr
        filestr=my_text.get(1.0,"end")
        print(filestr)
    
    def searchFileFE():
        savetag()
        global filestr
        filestr = filestr.strip('\n')
        filenames  = filestr.split(",")
        # print(filenames)
        matches = search_by_file_name(filenames)
        show_dialog(matches)
    
    for widget in frame2.winfo_children():
        widget.destroy()
    for widget in frame5.winfo_children():
        widget.destroy()
    frame2.pack_forget()
    frame5.pack_forget()

    left = Label(frame2, text="Enter the file's name to search")
    left.grid(row = 0,column=0,sticky='WE', padx=5, pady=5,columnspan=3)
    my_text=Text(frame2,width=20,height=2)

    my_text.grid(row = 1,column=0,sticky='WE', padx=5, pady=5,columnspan=3)
    my_text.grid_columnconfigure(0, weight=1)
    
    my_button2=Button(frame2,text="Clear", command=cleartextbox)
    my_button2.grid(row=2,column=0, padx=5, pady=2, sticky='E')
    my_button2=Button(frame2,text="Search", command=searchFileFE)
    my_button2.grid(row=2,column=1, padx=5, pady=2, sticky='E')
    # root.mainloop()

def searchfilebox():
    global filestr
    global w,h,x,y,x1searchname ,y1searchname ,w1searchname ,h1searchname,frame2

    class Checkbar(Frame):
        def __init__(self, parent, picks=[], side=LEFT, anchor=W):
            Frame.__init__(self, parent)
            i=0
            self.vars = []
            self.filenames = []

            for pick in picks:
                i=i+1
                var = IntVar(frame2)              
                chk = Checkbutton(self, text=pick, variable=var).grid(row=1,column = i)
                #  chk.pack(side=side, anchor=anchor, expand=YES)
                # self.update(var) 
                self.vars.append(var)
                self.filenames.append(pick)
                
            # left = Label(frame2, text="Search",font = "Calibri 12 italic")
            # left.grid(row = 1,column=i,sticky='NE', padx=5, pady=5)
            
        # def update(cls,value):
        #     cls.vars1.append(value)

    def state(cls):
            bool_var = map((lambda var: var.get()), cls.vars)
            from itertools import compress
            final_list = list(compress(cls.filenames,bool_var))
            return final_list

    def cleartextbox():
        global filestr
        my_text.delete(1.0,"end")
        filestr=''
        
    def savetag():
        global filestr
        filestr=my_text.get(1.0,"end")
    
    def searchFileFE():
        global filestr
        savetag()
        # print(state(scheck))
        # print(filestr)
        filestr = filestr.strip('\n')
        filenames  = filestr.split(",")
        searchcriteria = state(scheck)
        matches = pd.DataFrame(columns = ['original_file','pdf_file'])
        for i in searchcriteria:
            if i == 'Tags':
                matches =matches.append(search_by_tags(filenames))
                # show_dialog(matches)
            if i == 'Name':
                matches = matches.append(search_by_file_name(filenames))
            if i == 'User Tags':
                matches =matches.append(search_by_usertags(filenames))
            # if i == 'Date':
            #     # searchdatefromAllfunction()
            #     global fromdateselected,todateselected
            #     if fromdateselected == "":
            #         messagebox.showinfo("Disclaimer :","Please select To Date",parent = root)
            #     elif todateselected == "":
            #         messagebox.showinfo("Disclaimer :","Please select From Date",parent = root)

            if i == 'Type':
                matches =matches.append(search_by_file_type(filenames))
            if i == 'All':

                print("Search by All")
                matches =matches.append(search_by_tags(filenames))
                matches =matches.append(search_by_file_name(filenames))
                matches =matches.append(search_by_usertags(filenames))

            # unique_matches = list(dict.fromkeys(matches['original_file'].tolist()))
            # unique_pdf_matches = list(dict.fromkeys(matches['pdf_file'].tolist()))
            # result = set(x for l in matches['original_file'].tolist() for x in l)
            # print(result)
            show_dialog(matches)

    for widget in frame2.winfo_children():
        widget.destroy()
    
    frame2.pack_forget()

    scheck = Checkbar(frame2, ['All','Name','Tags','User Tags','Date','Type'])

    scheck.grid(row=1)
    scheck.config(relief=GROOVE, bd=2)

    my_text=Text(frame2,width=20,height=2)
    my_text.grid(row = 2,column=0,sticky='WE', padx=5, pady=5,columnspan=4)
    my_text.grid_columnconfigure(0, weight=1)
    
    left = Label(frame2, text="Enter multiple keywords separated by comma", font = "Calibri 10 italic")
    left.grid(row = 3,column=0,sticky='WE', padx=5, pady=5)

    my_button2=Button(frame2,text="Clear", command=cleartextbox)
    my_button2.grid(row=4,column=0, padx=5, pady=2, sticky='W')
    
    my_button2=Button(frame2,text="Search", command=searchFileFE)
    my_button2.grid(row=4,column=1, padx=5, pady=2, sticky='E')

    # root.mainloop()

def clientdetails():
    left = Label(frame4, text="Client Details*: Heena", font = "Calibri 10 italic")
    left.grid(row = 1,column=0,sticky='W', padx=5, pady=5)

    left = Label(frame4, text="Date Range*: 2019-2020", font = "Calibri 10 italic")
    left.grid(row = 1,column=2,sticky='W', padx=5, pady=5)

def callall():
    searchfilebox()
    searchdate(frame5)

def calldatemenu():
    for widget in frame5.winfo_children():
        widget.destroy()
    frame5.pack_forget()
    searchdate(frame2)

def hello():
    print ("hello!")

def About():
    messagebox.showinfo("About","CA Documentum for you to store and retrieve your documents and do much more.",parent = root)

root = Tk()
root.title("CA Documentum")
# root.geometry("1200x1200")

w = 800 # width for the Tk root
h = 500 # height for the Tk root

ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
print(ws,hs,w,h)
# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.attributes('-fullscreen', False)
# print(w, h, x, y)


#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#"""""""""                                      FRAME 4                                 """""""""""
#"""""""""                                      FRAME 2    FRAME 5                      """""""""""
#"""""""""               FRAME 1                                 FRAME3                 """""""""""
#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


frame4 = Frame(root,width=w, height=0.5*h/5)#,background = '#F7DC6F')
frame4.grid(row = 0,columnspan=2)
frame4.config(highlightbackground="black", highlightthickness=1)

frame5 = Frame(root,width=w/2, height=2.5*h/5)
frame5.grid(row = 1,column=1)
frame5.config(highlightbackground="black")

frame2 = Frame(root,width=w/2, height=2.5*h/5)#,background = '#F7DC6F')
frame2.grid(row = 1,column=0)
frame2.config(highlightbackground="black")

frame1 = Frame(root,width=w/2, height=2*h/5)
frame1.grid(row = 2,column=0)
frame1.config(highlightbackground="black",highlightthickness=1 )

frame3 = Frame(root,width=w/2, height=2*h/5)
frame3.grid(row = 2,column=1)
frame3.config(highlightbackground="black", highlightthickness=1)


frame1.grid_propagate(0)
frame2.grid_propagate(0)
frame3.grid_propagate(0)
frame4.grid_propagate(0)
frame5.grid_propagate(0)

menubar = Menu(frame1)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Upload", command=UploadFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Document Upload", menu=filemenu)

# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Search by Name", command=searchfile)
editmenu.add_command(label="Search by Tags", command=searchtag)
editmenu.add_command(label="Search by Date", command=calldatemenu)
editmenu.add_command(label="Generic Search", command=callall)

menubar.add_cascade(label="Document Search", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=About)
menubar.add_cascade(label="Help", menu=helpmenu)

#Frame1 
UploadFile()
#Frame2
searchfilebox()
#Frame4
clientdetails()
#Frame5
searchdate(frame5)


# display the menu
root.config(menu=menubar)
root.mainloop()
# root.quit()
# root.destroy()