from PIL import Image as im
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys
import numpy as np
import imageio.v3 as iio
import ipympl
import matplotlib.pyplot as plt
import skimage as ski
import skimage.feature
import pandas as pd
import scipy.stats as stats
from scipy.stats import entropy
from skimage import feature, measure
from skimage.measure import label, regionprops, regionprops_table
import pyarrow.parquet as pa
import string
from openpyxl import load_workbook
from openpyxl import Workbook
import openpyxl
import csv
import cv2
import json
from statistics import mode

#This is the code that belongs to Olorogun Engineer Enoch O. Ejofodomi in his Collaboration with Shell Onward.
#This code also belongs to Engineer Francis Olawuyi in his collaboration with Shell Onward.
#The code also belongs to the following people
#1. Esther Olawuyi
#2. Michael Olawuyi.
#3. Joshua Olawuyi
#4. Joseph Olawuyi
#5. Onome Ejofodomi
#6. Efejera Ejofodomi
#7. Deborah Olawuyi
#8. Isi Omiyi
#9. Kome Odu
#10. Sunday Damilola Olawuyi
#11. Godswill Ofualagba
#12. Matthew Olawuyi
#13. Jason Zara
#14. Vesna Zderic
#15. Ahmed Jendoubi
#16. Mohammed Chouikha
#17. Shani Ross
#18. Nicholas Monyenye
#19. Ochamuke Ejofodomi
#20. 
# APRIL 11, 2024.



#Read in File with User Electricity Consumption Data
table = pa.read_table('3.parquet') 
table
table.shape
df = table.to_pandas() 
# Taking tanspose so the printing dataset will easy. 
df.head().T
data2 = df.head().T
print(data2)
data = df.head()
tcolumns = table.num_columns
trows = table.num_rows
column1 = table.columns[0]
data.size
data.shape
print(data)


data1 = np.array(data)
imageppp = np.asanyarray(data)
print(imageppp)
np.save('1.txt',data)
#print(df.head().T[1])


#Read in Electricity Consumption Data for 2019
df = pd.read_parquet('1276.parquet')

#Convert file from parquet to csv in excel
df.to_csv('1.csv')

#Read CSV file
datacsv = pd.read_csv("1.csv")

#Geg Shape of Data in File
datacsv.shape

#Print Data
print(datacsv)

#Get Shape of CSV Data
[a,b] =  datacsv.shape
datacsv.values[0,1]

#Morning Values for January 1, 2018 : 6 a.m. - 12 p.m. is [23] - [47]
#Afternoon Values: 12 p.m. - 7 p.m. is [47] - [75]
#Evening Values: 7 p.m. - 6 a.m. (7-12 & 12-6) -> [75] - [95] & [0] - [23]

#Morning Values for January 2, 2018 : 6 a.m. - 12 p.m. is [119] - [143]
#Afternoon Values: 12 p.m. - 7 p.m. is [143] - [171]
#Evening Values: 7 p.m. - 6 a.m. (7-12 & 12-6) -> [171] - [191] & [95] - [119]

#Morning Values for January 2, 2018 : 6 a.m. - 12 p.m. is [+96] - [+96]
#Afternoon Values: 12 p.m. - 7 p.m. is [96] - [96]
#Evening Values: 7 p.m. - 6 a.m. (7-12 & 12-6) -> [96] - [96] & [96] - [96]




# The Electricity Consumption Data runs through out 2018 in 15 minute segments.
# Get The Electrcity Consumption for the Month of January Only and use that
# for Load Profile Analysis

january = datacsv.values[0:2975,:]


#Get shape of January Data
[a1,b1] =  january.shape


#Extract Total Energy Consumption from Data
januaryconsumption = january[:,2];
print(januaryconsumption)

#Get shape of January Consumption
[a2] =  januaryconsumption.shape
print(a2)



# MAXIMUM CONSUMPTION = X
# MINIMUM CONSUMPTON = Y
# HIGH IS >= 70% OF MAXIMUM CONSUMPTION VALUE ACROSS JANUARY
# LOW IS <70% OF MAXIMUM CONSUMPTION VALUE ACROSS JANUARY
maxconsumption = max(januaryconsumption)
minconsumption = min(januaryconsumption)

print(maxconsumption)
print(minconsumption)
start = 0
sumdata = 0
morningdata = np.zeros((31))
afternoondata = np.zeros((31))
evening1data = np.zeros((31))
evening2data = np.zeros((31))

for j in range(0,31):
    for k in range(start,start+96):
        sumdata = 0
        for m in range(start, start+23):
            #print(januaryconsumption[m])
            if(januaryconsumption[m] >= 0.7 * maxconsumption):
                sumdata = sumdata + 1
            if(sumdata == 24):
                evening2data[j]= 1
        sumdata = 0
        for m in range(start+75, start+95):
            if(januaryconsumption[m] >= 0.7 * maxconsumption):
                sumdata = sumdata + 1
                if(sumdata == 24):
                    evening1data[j]= 1
        sumdata = 0
        for m in range(start+45, start+75):
            if(januaryconsumption[m] >= 0.7 * maxconsumption):
                sumdata = sumdata + 1
                if(sumdata == 24):
                    afternoondata[j]= 1        
        sumdata = 0
        for m in range(start+23, start+47):
            if(januaryconsumption[m] >= 0.7 * maxconsumption):
                sumdata = sumdata + 1
                if(sumdata == 24):
                    morningdata[j]= 1
        
    

    start = start +96
print("Results")
print("Morning Data")
print(morningdata)
print("Afternoon Data")
print(afternoondata)
print("Evening 1 Data")
print(evening1data)
print("Evening 2 Data")
print(evening2data)
 
eveningdata = evening1data + evening2data
for j in range(0,31):
    if(eveningdata[j] == 1):
        eveningdata[j] = 0
    if(eveningdata[j] == 2):
        eveningdata[j] = 1

morningdata_mode = mode(morningdata)
afternoondata_mode = mode(afternoondata)
eveningdata_mode = mode(eveningdata)

print(morningdata_mode)
print(afternoondata_mode)
print(eveningdata_mode)


# GET USER LOAD PROFILE
# The Electricity Consumption Load Profiles that we have designed are as follows:
# 1. RESIDENTIAL:- ALL NIGHT HIGH CONSUMPTION
# 2. INUDSTIRAL/COMMERCIAL:- ALL DAY HIGH CONSUMPTION
# 3. MAXIMUM CONSUMER:- ALL DAY AND NIGHT HIGH CONSUMPTION (TRANSFORMATION SYSTEMS & SUBWAYS, POWER GENERATING SYSTEMS)
# 4. EARLY BIRD:- ALL MORNING HIGH (PEOPLE THAT WORK NIGHT HOURS AND SLEEP AT DAY)
# 5. HIGH PROFILE:- ALL FTERNOON HIGH - BUILDINGS THAT OPERATE WITH PHOTOVOLTAIC POWER SOURCES
# 6. MINIMUM CONSUMER:- STRAIGHT-LINE CONSUMER WITH LOW CONSUMPTION VALLUES
# 7. LOW PROFILE CONSUMER - NO HIGH CONSUMPTION

LOADPROFILE = 8

if((morningdata_mode == 0) & (afternoondata_mode == 0) & (eveningdata_mode == 0)):
    #USER IS LOW PROFILE CONSUMER
    LOADPROFILE = 7

if((morningdata_mode == 0) & (afternoondata_mode == 0) & (eveningdata_mode == 1)):
    #USER IS RESIDENTIAL
    LOADPROFILE = 1
    
if((morningdata_mode == 0) & (afternoondata_mode == 1) & (eveningdata_mode == 0)):
    #USER IS HIGH ROFILE CONSUMER
    LOADPROFILE = 5

if((morningdata_mode == 1) & (afternoondata_mode == 1) & (eveningdata_mode == 0)):
    #USER IS INDUSTRIAL/COMMERCIAL
    LOADPROFILE = 2

if((morningdata_mode == 1) & (afternoondata_mode == 0) & (eveningdata_mode == 0)):
    #USER IS EARLY BIRD CONSUMER
    LOADPROFILE = 4


straightlinetest = maxconsumption - minconsumption

if(straightlinetest <= 2):
    # USER HAS A STRAIGHT LINE PROFILE OR FLAT LINE IF MAX-MIN < 2KWH
    #SET AS MAXIMUM CONSUMER
    LOADPROFILE = 3
    if(maxconsumption < 2):
        #USER IS A MINIMUM CONSUMER if MAX CONSUMPTION < 2KWH
        LOADPROFILE = 6

#(If (maxconsumption = minconsumption) <= a certain value
#    => straight line (flat line)
#   Set Consumer Profile = 3 (MAXIMUM CONSUMER)
#   If (maxconsumption <= certain value)
#    => Set Profile 6 (MINIMUM CONSUMER)

print("FINAL LOAD PROFILE FOR USER:")
print(LOADPROFILE)
LOADPROFILE_STRING = ["RESIDENTIAL CONSUMER", "INDUSTRIAL/COMMERCIAL CONSUMER", "MAXIMUM CONSUMER", "EARLY BIRD CONSUMER", "HIGH PROFILE CONSUMER", "MINIMUM CONSUMER", "LOW PROFILE CONSUMER" ]
if(LOADPROFILE == 1):
    print(LOADPROFILE_STRING[0])
if(LOADPROFILE == 2):
    print(LOADPROFILE_STRING[1])
if(LOADPROFILE == 3):
    print(LOADPROFILE_STRING[2])
if(LOADPROFILE == 4):
    print(LOADPROFILE_STRING[3])
if(LOADPROFILE == 5):
    print(LOADPROFILE_STRING[4])
if(LOADPROFILE == 6):
    print(LOADPROFILE_STRING[5])
if(LOADPROFILE == 7):
    print(LOADPROFILE_STRING[6])

                      
                      
#   Work on Display, Programs for 7 Load Profiles, User Input to Load Electricity Consumption


