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
from statistics import mean

#This is the code that belongs to Olorogun Engineer Enoch O. Ejofodomi in his Collaboration with Shell Onward.
#This code also belongs to Engineer Francis Olawuyi in his collaboration with Shell Onward.
#The code also belongs to the following people
#1. GODSWILL OFUALAGBA C.E.O. SWILLAS ENERGY LIMITED.
#2. DR. MICHAEL OLAWUYI
#3. DR. DAMILOLA SUNDAY OLAWUYI
#4. ENGINEER DEBORAH OLAWUYI
#5. ENGINEER JOSHUA OLAWUYI
#6. ENGINEER JOSEPH OLAWUYI
#7. ENGINEER ONOME EJOFODOMI
#8. ENGINEER EFEJERA EJOFODOMI
#9. ENGINEER FRANCIS OLAWUYI
#10. DR. MATTHEW OLAWUYI
#11. ENGINEER ENOCH O. EJOFODOMI
#12. OCHAMUKE EJOFODOMI
#13. ENGINEER ONOME OMIYI
#14. MS. KOME ODU
#15. MR. KAYODE ADEDIPE
#16. MR. OMAFUME EJOFODOMI
#17. MR. NICHOLAS MONYENYE
#18. ENGINEER AYO ADEGITE
#19. ENGINEER ESOSA EHANIRE
#20. Ms. NANAYE INOKOBA
#21. Ms. YINKA OLAREWAJU-ALO
#22. Ms. ERKINAY ABLIZ
#23. Ms. FAEZEH RAZOUYAN
#24. MRS. TEVUKE EJOFODOMI
#25. MR.ONORIODE AGGREH
#26. MS. NDIDI IKEMEFUNA
#27. MS. ENAJITE AGGREH
#28. DR. ESTHER OLAWUYI
#29  MS. ISI OMIYI
#30. DR. JASON ZARA
#31. DR. VESNA ZDERIC
#32. DR. AHMED JENDOUBI
#33. DR. MOHAMMED CHOUIKHA
#34. MS. SHANI ROSS


# APRIL 15, 2024.


#Get Electricity Consumption File from User and Read in File with User Electricity Consumption Data
ConsumptionDataFile = input("Enter the parquet file name that holds the User's Electricity Consumption Data e.g. 2.parquet :- ")
print("You entered: ")
print((ConsumptionDataFile))
InputConsumptionDataFile =ConsumptionDataFile


table = pa.read_table(InputConsumptionDataFile) 
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



#Read in User Electricity Consumption Data
df = pd.read_parquet(InputConsumptionDataFile)
strlen = len(InputConsumptionDataFile)
StringCSVFile = InputConsumptionDataFile[0:strlen-7]
print("StringCSVFile: ")
print(StringCSVFile)
StringCSVFile = StringCSVFile + "csv"
print("StringCSVFile: ")
print(StringCSVFile)

#Convert file from parquet to csv in excel
df.to_csv(StringCSVFile)

#Read CSV file
datacsv = pd.read_csv(StringCSVFile)

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




# In our Test Files, The Electricity Consumption Data runs through out 2018 in 15 minute segments.
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


#Extract Time Stamp from Energy Consumption Data
timestamp = january[:,1];
print(timestamp)

for j in range(0,a2):
    timestamp1 = timestamp[j]
    timestamp[j] = timestamp1[11: len(timestamp1)]
print("timestamp")
print(timestamp)


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
y2 = [0,0,0,0,0]
CHARTTITLE = ""
LOADPROFILE_STRING = ["RESIDENTIAL CONSUMER", "INDUSTRIAL/COMMERCIAL CONSUMER", "MAXIMUM CONSUMER", "EARLY BIRD CONSUMER", "HIGH PROFILE CONSUMER", "MINIMUM CONSUMER", "LOW PROFILE CONSUMER" ]
if(LOADPROFILE == 1):
    print(LOADPROFILE_STRING[0])
    CHARTTITLE = LOADPROFILE_STRING[0]
    y2 = [maxconsumption,((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2),maxconsumption,maxconsumption]
if(LOADPROFILE == 2):
    print(LOADPROFILE_STRING[1])
    CHARTTITLE = LOADPROFILE_STRING[1]
    y2 = [((maxconsumption-minconsumption)/2),maxconsumption,maxconsumption,((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2)]
if(LOADPROFILE == 3):
    print(LOADPROFILE_STRING[2])
    CHARTTITLE = LOADPROFILE_STRING[2]
    y2 = [maxconsumption,maxconsumption,maxconsumption,maxconsumption,maxconsumption]
if(LOADPROFILE == 4):
    print(LOADPROFILE_STRING[3])
    CHARTTITLE = LOADPROFILE_STRING[3]
    y2 = [((maxconsumption-minconsumption)/2),maxconsumption,((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2)]
if(LOADPROFILE == 5):
    print(LOADPROFILE_STRING[4])
    CHARTTITLE = LOADPROFILE_STRING[4]
    y2 = [((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2),maxconsumption,((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2)]
if(LOADPROFILE == 6):
    print(LOADPROFILE_STRING[5])
    CHARTTITLE = LOADPROFILE_STRING[5]
    y2 = [maxconsumption,maxconsumption,maxconsumption,maxconsumption,maxconsumption]
if(LOADPROFILE == 7):
    print(LOADPROFILE_STRING[6])
    CHARTTITLE = LOADPROFILE_STRING[6]
    y2 = [((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2)]


#Plot Lomaded User Profile to see
xaxis = range(2975)
consumption_mean = mean(januaryconsumption)
x1 = [0,2975]
y1 = [consumption_mean, consumption_mean]
plt.plot(xaxis,januaryconsumption, label = "Consumer Data", color='green', linewidth = 6)
plt.plot(x1, y1, label = "Average Monthly Consumtion", color='red', linewidth = 6)
plt.xlim(0,2976)
plt.xlabel('Time in 15 MINUTE SEGMENTS')
plt.ylabel('ELECTRICITY CONSUMED (KWh)')
plt.title("LOAD PROFILE FOR ELECTRICITY CONSUMER - " + CHARTTITLE ) 
# show a legend on the plot
plt.legend()
plt.show()                      
#3.parquet

xaxis2= range(30)
x2= [0,23,47,75, 95]
plt.plot(x2, y2, label = CHARTTITLE + " LOAD PROFILE", color='blue', linewidth = 6)
plt.xlim(0,24)
plt.xlabel('Time in 15 MINUTE SEGMENTS for ONE FULL DAY')
plt.ylabel('ELECTRICITY CONSUMED (KWh)')
plt.title(CHARTTITLE + " LOAD PROFILE") 
# show a legend on the plot
plt.legend()
plt.show()

# line 1 points
#x1 = [1,2,3]
#y1 = [2,4,1]
# plotting the line 1 points 
#plt.plot(x1, y1, label = "line 1")
 
# line 2 points
#x2 = [1,2,3]
#y2 = [4,1,3]
# plotting the line 2 points 
#plt.plot(x2, y2, label = "line 2")#import numpy      p
#myLost= np.linespace(0, 100 n) generate n consecutive numbers in
#equal intervals between them starting from 0 to 100

#   Work on
#  1. Load Profile Display,
#  2. Programs for 7 Load Profiles, 

