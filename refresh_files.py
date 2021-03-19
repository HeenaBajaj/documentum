
import os
import datetime
import pandas as pd
import re
#userfiles
from SQL_Conn import *
from doc_functions import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

originalfilepath = BASE_DIR + '\\Original Files\\' 

files_modtime ='''select distinct file_name,modified_date from FileDetails'''
df1= pd.read_sql(files_modtime, conn)
# print(df1['file_name'])
        
with os.scandir(originalfilepath) as dir_contents:
    for entry in dir_contents:
        current_mod_time =datetime.datetime.fromtimestamp(os.stat(originalfilepath+entry.name).st_mtime)
        filename = entry.name.split(".")[0]
        #Existing Files
        df = df1.loc[df1['file_name']==filename]
        dftime = df['modified_date']
        for i in dftime:
            last_modified_date = datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S.%f')
            if current_mod_time > last_modified_date:
                filepath = originalfilepath+entry.name
                # print(filepath)
                fileUpload(filepath,usertags,1,0,1,'')

all_files = pd.DataFrame(columns = ['file','name'])

with os.scandir(originalfilepath) as dir_contents:
    for entry in dir_contents:
        all_file = pd.DataFrame(columns = ['file','name'])
        all_file['file'] = [entry.name]
        all_file['name'] = [entry.name.split(".")[0]]
        all_files = all_files.append(all_file)

# print(all_files)
# all_files_Series = pd.Series(all_files)
new_files = all_files[~all_files['name'].isin(df1['file_name'])]

for j in new_files['file']:
    filepath = originalfilepath + j
    fileUpload(filepath,usertags,1,0,0,'')


