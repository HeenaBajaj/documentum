import os
import sys
import shutil, sys  
import pytesseract
from pytesseract import Output
import subprocess
from fpdf import FPDF 
from subprocess import  Popen
from cv2 import cv2
import PyPDF2
from xlrd import open_workbook
import csv
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
# from DocumentumFrontend import UploadFile as dfe
# import DocumentumFrontend as dfe

#userfiles
from SQL_Conn import *


strfil = ''
filepath = ''
todateselected = ''
fromdateselected = ''
x = 0
y = 0
w = 0
h = 0
usertags = ''

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_conn = BASE_DIR + '\\' + r"pythonsqlite.db"

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
################   Convert uploaded document to text file to create tags  ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def pdftotext(file_path):
  
  img_type = file_path.split(".")[1]
  #   APP_ROOT = os.path.abspath(documentum.__path__[0])
  #   file_path=getrootpath(img_url)
  #   # print('',file_path)
  # file_path = os.path.join('C:/Users/ASUS/Desktop/project/documentum/'+str(img_url))

  if img_type=="pdf":
      pdf_file = open(file_path,'rb')
      read_pdf = PyPDF2.PdfFileReader(pdf_file)
      number_of_pages = read_pdf.getNumPages()
      page_content=""
      for i in range(number_of_pages):
          page = read_pdf.getPage(i)
          content = page.extractText()
          page_content+=content
    #   text_list= page_content.split(" ")
    #   text_word= [word for word in text_list if word not in stop_words] 
    #   text_remove_rep=list(set(text_word))
    #   print(pageObj.extractText()) 
    #   print(text_remove_rep)
      return page_content
      
  elif img_type=="jpg" or img_type=="jpeg" or img_type=="png":
    #   img = cv2.imread(r'C:\Users\A118090\OneDrive - AXAXL\Desktop\hello_django\PyQT\Izoe\CADocumentum\bc.jpg')
      img = cv2.imread(file_path)
      img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      pytesseract.pytesseract.tesseract_cmd = r'C:\Users\A118090\AppData\Local\Programs\Python\Python36\Lib\site-packages\pytesseract-0.3.5-py3.6.egg-info\tesseract-ocr-setup-3.02.02.exe'
      from PIL import Image
      tesseract_output = pytesseract.image_to_string(Image.fromarray(img),lang="eng")
    #   print(pytesseract.image_to_string(r'C:\Users\A118090\OneDrive - AXAXL\Desktop\hello_django\PyQT\Izoe\CADocumentum\bc.jpg'))
      text=tesseract_output
      return text

  elif img_type=="doc" or img_type=="docx":
    fullText=[]
    # print("----- This is file path here -----")
    # print(file_path)
    document = Document(file_path)
    for para in document.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
    
  elif img_type=="txt":
    text_file=open(file_path,'r')
    text=text_file.read()
    return text

  elif img_type=="csv":
    text=[]
    string_list=[]
    string_seq=""
    with open(file_path,'rt')as f:
      data = csv.reader(f)
      for row in data:
        text.append(row)
    
    for text_list in text:
      string_list=string_list + text_list
    for string in string_list:
      string_seq+=string

    return string_seq

  elif img_type=="xlsx" or img_type=="xlsm" or img_type=="xls":  
    book = open_workbook(file_path)
    sheet = book.sheet_by_index(0)
    # read header values into the list    
    keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]
    dict_list = []
    for row_index in range(1, sheet.nrows):
        d = {keys[col_index]: sheet.cell(row_index, col_index).value 
            for col_index in range(sheet.ncols)}
        dict_list.append(d)

    all_dict=[]
    for d in dict_list:
      for k, v in d.items():
        all_dict.append(k)
        all_dict.append(v)

    if '' in all_dict:
      all_dict.remove('')
    else:
      pass
     
    string_list=""
    string_list=','.join(str(s) for s in all_dict)
    text=string_list
    return text
  else:
    text="file format does not match"
    return text   
 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
################################## Create tags using nltk  ##################################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def get_tags(text):
  sentences = nltk.sent_tokenize(text) 
  nouns = []
  for sentence in sentences:
    tokenizer = RegexpTokenizer(r'\w+') 
    for word,pos in nltk.pos_tag(tokenizer.tokenize(sentence)):
      if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' ):
        nouns.append(word)            
  return nouns
  #     for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
  #       if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' ):
  #         nouns.append(word)         
  # return nouns
  
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
################################## Convert documents in pdf format  #########################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# convert from a file to PDF automatically
def ConvertToPdfFromFile(file_path,output_path):
    img_type = file_path.split(".")[1]
    if img_type=="jpg" or img_type=="jpeg" or img_type=="png":
        from PIL import Image
        image = Image.open(file_path)
        pdf_bytes = img2pdf.convert(image.filename) 
        file = open(output_path, "wb") 
        file.write(pdf_bytes)
        image.close()
        file.close() 
    elif img_type=="doc" or img_type=="docx":
        from docx2pdf import convert
        convert(file_path, output_path)
    elif img_type=="txt":
        pdf = FPDF()      
        # Add a page 
        pdf.add_page()         
        # set style and size of font  
        # that you want in the pdf 
        pdf.set_font("Arial", size = 15)        
        # open the text file in read mode 
        f = open(file_path, "r")   
        # insert the texts in pdf 
        for x in f: 
            pdf.cell(200, 10, txt = x, ln = 1, align = 'C') 
        # save the pdf with name .pdf 
        pdf.output(output_path) 
        
    elif img_type=="csv":
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Users\A118090\AppData\Local\Programs\Python\Python36\Lib\site-packages\wkhtmltopdf')
        pdfkit.from_file(file_path,
                 output_path,
                 configuration=config
                )

    elif img_type=="xlsx" or img_type=="xlsm" or img_type=="xls":  
        from win32com import client
        xlApp = client.Dispatch("Excel.Application")
        books = xlApp.Workbooks.Open(file_path)
        # ws = books.Worksheets[0]
        # ws.Visible = 1
        # ws.ExportAsFixedFormat(0, output_path)
        ws_index_list = []
        r1=1
        while(r1 <= books.Worksheets.Count ): 
              
            ws_index_list.append(r1) 
            r1 += 1
        # print(ws_index_list)  
        books.WorkSheets(ws_index_list).Select()
        # # Save
        books.ActiveSheet.ExportAsFixedFormat(0, output_path)
        books.Close(True,file_path)
        print("file_path closed..")
    else:
        text="file format does not match"
    
    print("Converted file: " + file_path + "\n\tto: " + output_path)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
##################  File Upload Backend Process: Creates various fields as File name, Original 
file location, Converted pdf file location, Created Date, Modified Date , Tags, 
Documents dates : Oldest and youngest date.##################################################

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def fileExists(filepath):
  conn = create_connection(db_conn)
  filename = os.path.basename(filepath)  #original File name
  qry="SELECT DISTINCT file_name from FileDetails" 
  conn.execute(qry)
  df1= pd.read_sql(qry, conn)
  if df1[df1['file_name'] == filename.split(".")[0]].empty ==0:
    return 1
  conn.commit()
  conn.close()
  
def deletefeatures(filepath):
  conn = create_connection(db_conn)
  filename = os.path.basename(filepath) 
  file_name = filename.split(".")[0]
  qry="delete from FileDetails where file_name = '%s'" %(file_name)
  conn.execute(qry)
  conn.commit()
  conn.close()



def fileUpload(filepath,usertags,refresh,existing_file,replace, rename):
  print("Uploading " + filepath)
  global BASE_DIR

  if replace ==1:
    #delete existing file properties from SQL. they will be reinserted in fileuploadtoSQL
    deletefeatures(filepath)

  file_type = filepath.split(".")[-1]
  path = os.path.abspath(filepath)
  file_urls = {}

  filename = os.path.basename(filepath)  #original File name
  print(filename)
  originalfiledir = BASE_DIR + '\\Original Files\\'

  #take the user defined name for the file
  if existing_file ==1:
    filename = rename + "." + file_type
    originalfilepath = originalfiledir + rename + "." + file_type
    print(originalfilepath)
  #take the original filename chose by user
  else : 
    filename = os.path.basename(filepath)  #original File name
    originalfilepath = originalfiledir + filename
  
  if not os.path.exists(originalfiledir):
        os.mkdir(originalfiledir)
        print("Directory " , originalfiledir ,  " Created ")

  if refresh == 0:
    from shutil import copystat,copyfile
    copyfile(filepath, originalfilepath)
    copystat(filepath, originalfilepath)
  
  print("Converting file to Pdf...")
  #CONVERT FILES TO PDF AND CONVERT to TEXT and create tags 

  if file_type == 'doc' or file_type == 'docx' or file_type == 'xlsx' or file_type == 'xls' or file_type == 'csv' or file_type == 'ppt' or file_type == 'pptx' or file_type == 'txt' or file_type == 'jpeg' or file_type == 'png' or file_type == 'jpg':
      # rename is the file getting renamed, pre is the part of file name before extension and ext is current extension
      # pre, ext = os.path.splitext(filepath)
      # filename = os.path.basename(filepath)  #original File name
      
      pdffiledir =  BASE_DIR + '\\Pdf Files\\' 
      
      if not os.path.exists(pdffiledir):
        os.mkdir(pdffiledir)
        print("Directory " , pdffiledir ,  " Created ")

      file_path = pdffiledir + filename     
      pre, ext = os.path.splitext(filename)   
      file_urls['file_name'] = pre      
      pre, ext = os.path.splitext(file_path)
      path =  pre + '.pdf'
      # file_urls.append(pre+'.pdf')   
      
      # file_urls['original_file'] = filepath
      originalfilepath = BASE_DIR + '\\Original Files\\' + filename
      file_urls['original_file'] = originalfilepath
      file_urls['pdf_file'] = path            #Pdf File path
      import time
      time.sleep(2)
  
      inputPath = filepath
      outputPath = path
      # testfiles = [filepath]

      #convert input file to pdf and store
      ConvertToPdfFromFile(inputPath,outputPath)

      print("Converted file to Pdf...")

      #convert original file to text 
      content = pdftotext(inputPath)

      print("Extracting details from file")

      #get tags from the file
      tags = get_tags(content)
      # file_urls['content'] = content
      file_urls['tags'] = tags
      file_urls['created_date'] = datetime.datetime.fromtimestamp(os.stat(filepath).st_ctime) #.date()
      file_urls['modified_date'] =datetime.datetime.fromtimestamp(os.stat(filepath).st_mtime) #.date()
      # dates = datefinder.find_dates(content)
      # for match in dates:
      #   print (match )

      dates= list()
      maxdates= list()
     
      dates.extend(re.findall("\d{4}[/-]\d{2}[/-]\d{2}", content))
      if len(dates)!=0:
        maxdates.append(max(dates))
        maxdates.append(min(dates))
      dates= list()
      dates.extend(re.findall("\d{2}[/-]\d{2}[/-]\d{4}", content))
      if len(dates)!=0:
        maxdates.append(max(dates))
        maxdates.append(min(dates))
      dates= list()
      dates.extend(re.findall("\d{2}[/-]\d{4}[/-]\d{2}", content))
      if len(dates)!=0:
        maxdates.append(max(dates))
        maxdates.append(min(dates))
      converteddates= list()

      if len(maxdates)==0:
         firstdate = []
      else:
        for date in maxdates:
          if "-" in date:
              month,day,year = map(int, date.split("-"))
          else:
              month,day,year = map(int, date.split("/"))
          if 1 <= day <= 31 and 1 <= month <= 12:
            date = datetime.datetime.strptime(date, '%m-%d-%Y').strftime('%Y-%m-%d')
            converteddates.append(date)

        for date in maxdates:
          if "-" in date:
              year,month,day  = map(int, date.split("-"))
          else:
              year,month,day  = map(int, date.split("/"))
          if 1 <= day <= 31 and 1 <= month <= 12:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
            converteddates.append(date)
              
        for date in maxdates:
          if "-" in date:
              month,year,day  = map(int, date.split("-"))
          else:
              month,year,day  = map(int, date.split("/"))
          if 1 <= day <= 31 and 1 <= month <= 12:
            date = datetime.datetime.strptime(date, '%m-%Y-%d').strftime('%Y-%m-%d')
            converteddates.append(date)
      youngest =[] 
      if len(converteddates) ==0:
        youngest = []
      else:
        youngest.append(max(converteddates))
        youngest.append(min(converteddates))
      file_urls['document_dates'] = youngest

  elif file_type == 'pdf':
      # rename is the file getting renamed, pre is the part of file name before extension and ext is current extension
      # pre, ext = os.path.splitext(filepath)
      # filename = os.path.basename(filepath)  #original File name
      pdffiledir =  BASE_DIR + '\\Pdf Files\\' 
      
      if not os.path.exists(pdffiledir):
        os.mkdir(pdffiledir)
        print("Directory " , pdffiledir ,  " Created ")

      file_path = pdffiledir + filename     

      pre, ext = os.path.splitext(filename)   
      file_urls['file_name'] = pre
      pre, ext = os.path.splitext(file_path)

      path =  pre + '.pdf'
      # file_urls.append(pre+'.pdf')   
      # file_urls['original_file'] = filepath

      originalfilepath = BASE_DIR + '\\Original Files\\' + filename
      file_urls['original_file'] = originalfilepath

      file_urls['pdf_file'] = path            #Pdf File path
      import time
      time.sleep(2)
  
      inputPath = filepath
      outputPath = path
      # testfiles = [file_path]

      #convert input file to pdf and store
      from shutil import copyfile
      copyfile(inputPath, outputPath)

      print("Extracting details from file")
      #convert original file to text 
      content = pdftotext(path)

      #get tags from the file
      tags = get_tags(content)
      # file_urls['content'] = content
      file_urls['tags'] = tags
      file_urls['created_date'] = datetime.datetime.fromtimestamp(os.stat(filepath).st_ctime) #.date()
      file_urls['modified_date'] =datetime.datetime.fromtimestamp(os.stat(filepath).st_mtime) #.date()

      dates= list()
      maxdates= list()
     
      dates.extend(re.findall("\d{4}[/-]\d{2}[/-]\d{2}", content))
      if len(dates)!=0:
        maxdates.append(max(dates))
        maxdates.append(min(dates))
      dates= list()
      dates.extend(re.findall("\d{2}[/-]\d{2}[/-]\d{4}", content))
      if len(dates)!=0:
        maxdates.append(max(dates))
        maxdates.append(min(dates))

      dates= list()
      dates.extend(re.findall("\d{2}[/-]\d{4}[/-]\d{2}", content))
      if len(dates)!=0:
        maxdates.append(max(dates))
        maxdates.append(min(dates))

      converteddates= list()

      if len(maxdates)==0:
         firstdate = []
      else:
        for date in maxdates:
          if "-" in date:
              month,day,year = map(int, date.split("-"))
          else:
              month,day,year = map(int, date.split("/"))
          if 1 <= day <= 31 and 1 <= month <= 12:
            date = datetime.datetime.strptime(date, '%m-%d-%Y').strftime('%Y-%m-%d')
            converteddates.append(date)

        for date in maxdates:
          if "-" in date:
              year,month,day  = map(int, date.split("-"))
          else:
              year,month,day  = map(int, date.split("/"))
          if 1 <= day <= 31 and 1 <= month <= 12:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
            converteddates.append(date)
              
        for date in maxdates:
          if "-" in date:
              month,year,day  = map(int, date.split("-"))
          else:
              month,year,day  = map(int, date.split("/"))
          if 1 <= day <= 31 and 1 <= month <= 12:
            date = datetime.datetime.strptime(date, '%m-%Y-%d').strftime('%Y-%m-%d')
            converteddates.append(date)
          
      # youngest = max(converteddates)
      if len(converteddates) ==0:
        youngest = []
      else:
        youngest.append(max(converteddates))
        youngest.append(min(converteddates))
      file_urls['document_dates'] = youngest
  
  else:
    print("File format not supported")

  username = getpass.getuser()
  file_urls['username'] = username
  # print(usertags)
  file_urls['usertags'] = usertags
  file_urls['type'] = file_type
  print(file_urls['file_name'])
  uploadFileDetailstoSql(file_urls)
  return file_urls

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
################################## File Information upload to SQL  ##########################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def uploadFileDetailstoSql(file_urls):
  
  conn = create_connection(db_conn)

  str1= list()
  for key,value in file_urls.items():
    value = str(value).replace("'", "$")
    str1.append(value)

  joined_string = "','".join(map(str,str1))
  joined_string = joined_string + "'"

  # print(joined_string)

  c = conn.cursor()
  qry="INSERT INTO FileDetails(file_name, original_file, pdf_file, tags, created_date, modified_date,document_dates,username,usertags,type) values('"+joined_string+")" 
  c.execute(qry)
  updatetable = "update FileDetails set tags = replace(tags,'$','''')"
  c.execute(updatetable )
  updatetable = "update FileDetails set document_dates = replace(document_dates,'$','''')"
  c.execute(updatetable )
  # select ='''select * from FileDetails'''
  # df1= pd.read_sql(select, conn)
  print("File uploaded to SQL")

  conn.commit()
  conn.close()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
################################## File search by name  ####################################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def search_by_file_name(filenames):
  
  conn = create_connection(db_conn)
  filenames_original ='''select distinct pdf_file,original_file,file_name from FileDetails'''
  c = conn.cursor()
  df1= pd.read_sql(filenames_original, conn)
  # df1= pd.Series(df1['file_name'])
  matches = pd.DataFrame(columns = ['original_file','pdf_file'])
  for i in range(len(filenames)):
    regex = filenames[i]
    for j in range(len(df1['file_name'])):
      # print(regex)
      match = re.search(regex,df1['file_name'][j],re.IGNORECASE)
      if match:
        if df1['original_file'][j] not in matches['original_file']:
          match = pd.DataFrame(columns = ['original_file','pdf_file'])
          match['original_file'] = [df1['original_file'][j]]
          match['pdf_file'] = [df1['pdf_file'][j]]
          matches = matches.append(match)

  matches = showFileName(matches)
  # print(matches)
  return matches
  conn.commit()
  conn.close()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
################################## File search by tag  ####################################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def search_by_tags(tags):
  conn = create_connection(db_conn)

  tags_original ='''select distinct pdf_file,original_file,file_name,tags from FileDetails'''
  c = conn.cursor()
  df1= pd.read_sql(tags_original, conn)
  # print(df1)
  # df1= pd.Series(df1['tags'])
  matches = pd.DataFrame(columns = ['original_file','pdf_file'])
  # print(df1['tags'])
  for i in range(len(tags)):
    regex = tags[i]
    
    for j in range(len(df1['tags'])):
      res = eval(df1['tags'][j])                                                          
      # print(res)
      for k in range(len(res)):
        match = re.search(regex,res[k],re.IGNORECASE)
        if match:
          if df1['original_file'][j] not in matches:
            match = pd.DataFrame(columns = ['original_file','pdf_file'])
            match['original_file'] = [df1['original_file'][j]]
            match['pdf_file'] = [df1['pdf_file'][j]]
            matches = matches.append(match)
  matches = showFileName(matches)
  return matches
  conn.commit()
  conn.close()


def search_by_usertags(tags):
  conn = create_connection(db_conn)
  tags_original ='''select distinct pdf_file,original_file,file_name,usertags from FileDetails'''
  c = conn.cursor()
  df1= pd.read_sql(tags_original, conn)
  # print(df1['usertags'])
  df1['usertags'] = df1['usertags'].fillna('dummy')
  # print(df1['usertags'])
  matches = pd.DataFrame(columns = ['original_file','pdf_file'])
  for i in range(len(tags)):
    regex = tags[i]
    for j in range(len(df1['usertags'])):
      res = df1['usertags'][j]
      match = re.search(regex,res,re.IGNORECASE)
      if match:
        if df1['original_file'][j] not in matches:
            match = pd.DataFrame(columns = ['original_file','pdf_file'])
            match['original_file'] = [df1['original_file'][j]]
            match['pdf_file'] = [df1['pdf_file'][j]]
            matches = matches.append(match)
  matches = showFileName(matches)
  return matches
  conn.commit()
  conn.close()
 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
################################## File search by tag date  #################################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def search_by_date(dates):
  conn = create_connection(db_conn)

  tags_original = '''select distinct pdf_file,original_file,file_name,created_date,modified_date,document_dates from FileDetails'''
  c = conn.cursor()
  df1= pd.read_sql(tags_original, conn)
  matches = pd.DataFrame(columns = ['original_file','pdf_file'])
  # for i in range(len(dates)):
  #   for j in range(len(df1['file_name'])):
  #     date_list = list()
  #     date_list.append(df1['created_date'][j])
  #     date_list.append(df1['modified_date'][j])
  #     date_list.append(df1['document_dates'][j])
  #     mylist = list(dict.fromkeys(date_list))                                                    
  #     if dates[i] in mylist:
  #         if dates[i] not in matches:
  #           matches.append(df1['file_name'][j])
  date_list = list()
  for j in range(len(df1['file_name'])):
      date_list = list()
      date_list.append(df1['created_date'][j])
      date_list.append(df1['modified_date'][j])
      res = eval(df1['document_dates'][j])    
     
      if res != []:
          date_list.extend(res)     
      mylist = list(dict.fromkeys(date_list))                                                 
      for k in range(len(mylist)):
        if dates[0] <mylist[k]<dates[1]:
            match = pd.DataFrame(columns = ['original_file','pdf_file'])
            match['original_file'] = [df1['original_file'][j]]
            match['pdf_file'] = [df1['pdf_file'][j]]
            matches = matches.append(match)

  # matches = list(dict.fromkeys(matches))  
  matches = showFileName(matches)
  return matches
  conn.commit()
  conn.close()


def search_by_file_type(filenames):
  conn = create_connection(db_conn)

  filenames_original ='''select distinct pdf_file,original_file,type from FileDetails'''
  c = conn.cursor()
  df1= pd.read_sql(filenames_original, conn)
  # df1= pd.Series(df1['file_name'])
  df1['Type'] = df1['Type'].fillna('dummy')
  matches = pd.DataFrame(columns = ['original_file','pdf_file'])
  for i in range(len(filenames)):
    regex = filenames[i]
    for j in range(len(df1['Type'])):
      match = re.search(regex,df1['Type'][j],re.IGNORECASE)
      if match:
        if df1['original_file'][j] not in matches:
            match = pd.DataFrame(columns = ['original_file','pdf_file'])
            match['original_file'] = [df1['original_file'][j]]
            match['pdf_file'] = [df1['pdf_file'][j]]
            matches = matches.append(match)

  matches = showFileName(matches)
  return matches
  
  conn.commit()
  conn.close()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
################################## Filesearch above gives file name, file location is given 
by below function                                           #################################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def showFileName(matches):
  return matches

# filepath = r"C:\\Users\\A118090\\OneDrive - AXAXL\\Desktop\\hello_django\\PyQT\\ProjI\\CADocumentum\\Documents\\test.xlsx"
# fileUpload(r"C:\Users\A118090\OneDrive - AXAXL\Desktop\hello_django\PyQT\ProjI\CADocumentum\Documents\Ref_TicketNumber.pdf",'heena',1,0,"bowse123")
# fileExists(filepath)
