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


# APRIL 18, 2024.


#Get Electricity Consumption File from User and Read in File with User Electricity Consumption Data
# The software allows you to automatically select and load the user profile data for which you want to run the analysis on.
#Here, the software asks you to enter in the name of the file containing the consumers electricity profile in order to
#cluster the load profile.
ConsumptionDataFile = input("Enter the parquet file name that holds the User's Electricity Consumption Data e.g. 2.parquet :- ")
print("You entered: ")
print((ConsumptionDataFile))
InputConsumptionDataFile =ConsumptionDataFile


#The input data is concerted to tabular form so it can be read by the algorithm.
#The sice and data of the table is obtained
table = pa.read_table(InputConsumptionDataFile) 
table
table.shape
df = table.to_pandas()  
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



#The code begins reading in the User Electricity Consumption Data
df = pd.read_parquet(InputConsumptionDataFile)
strlen = len(InputConsumptionDataFile)
StringCSVFile = InputConsumptionDataFile[0:strlen-7]
print("StringCSVFile: ")
print(StringCSVFile)
StringCSVFile = StringCSVFile + "csv"
print("StringCSVFile: ")
print(StringCSVFile)

#The Data is Converted from parquet file to csv in excel
df.to_csv(StringCSVFile)

#The CSV file is read
datacsv = pd.read_csv(StringCSVFile)

#Acquire the Shape of Shape of the Data in File
datacsv.shape

#Print the Data
print(datacsv)

#Get Shape of CSV Data and store it in variables
[a,b] =  datacsv.shape
datacsv.values[0,1]

#Observations from the File
# the 15 Minute Segment of Electricity Consumption Data runs throughout the year.
# The input Values for a Single Month are noted
# The Input Values Needed to access the Electricity Consumption Data Month by Month
# is determined to be in Data Increments of +96, as shown below:

#Morning Values for January 1, 2018 : 6 a.m. - 12 p.m. is [23] - [47]
#Afternoon Values: 12 p.m. - 7 p.m. is [47] - [75]
#Evening Values: 7 p.m. - 6 a.m. (7-12 & 12-6) -> [75] - [95] & [0] - [23]

#Morning Values for January 2, 2018 : 6 a.m. - 12 p.m. is [119] - [143]
#Afternoon Values: 12 p.m. - 7 p.m. is [143] - [171]
#Evening Values: 7 p.m. - 6 a.m. (7-12 & 12-6) -> [171] - [191] & [95] - [119]

#Morning Values for January 2, 2018 : 6 a.m. - 12 p.m. is [+96] - [+96]
#Afternoon Values: 12 p.m. - 7 p.m. is [96] - [96]
#Evening Values: 7 p.m. - 6 a.m. (7-12 & 12-6) -> [96] - [96] & [96] - [96]




# In the Test Files used to train the algorithm, The Electricity Consumption Data
# runs through out 2018 in 15 minute segments.
# For the Analysis of the Load Profile for a Single Consumer, we determined that
# 15 Minute Segment Data running for a full month would be sufficien to perform
# accurate load profile clustering for the consumer.
# So, we get The Electrcity Consumption Data of the Consumer for the FIRST MONTH
# ONLY (e.g. January) and use that to Cluster the Load Profile.

january = datacsv.values[0:2975,:]


#Get shape of Month Data
[a1,b1] =  january.shape


#Extract Total Energy Consumption from the Month Data
januaryconsumption = january[:,2];
print(januaryconsumption)


#Get shape of Month Consumption Data
[a2] =  januaryconsumption.shape
print(a2)


#Extract Time Stamp (in 15 Minute Segements) from Energy Consumption Data
timestamp = january[:,1];
print(timestamp)

for j in range(0,a2):
    timestamp1 = timestamp[j]
    timestamp[j] = timestamp1[11: len(timestamp1)]
print("timestamp")
print(timestamp)


#LOAD PROFILE CLUSTERING ALGORITHM
# We determined that we would need  2 important variables:
# 1. To hold the Maximum Energy Consumption of the Consumer
# 2. To hold the Minimum Energy Consumption of the Consumer

# MAXIMUM CONSUMPTION = X
# MINIMUM CONSUMPTON = Y
maxconsumption = max(januaryconsumption)
minconsumption = min(januaryconsumption)

print(maxconsumption)
print(minconsumption)

# We determined that if an Energy Consumption Value was higher
# than 70% of the Maximum Energy Consumed by the User, then
# that energy was regrded as a HIGH Consumption.
# Conversely, if an Energy Consumption Value was lower than
# 70% of the Maximum Energy Consumed by the User, then that
# energy was regarded as a LOW Consumption.
# HIGH IS >= 70% OF MAXIMUM CONSUMPTION VALUE ACROSS MONTH
# LOW IS <70% OF MAXIMUM CONSUMPTION VALUE ACROSS MONTH



#VARIABLE DEFINITIONS
# The start variable is used to run through the Electricity Data in
# increments of 96, as each 96 segment of Data represents the
# Electricity Consumption of the User for ONE FULL DAY.
start = 0
# The sumdata variable is used to run through the Electricity Data in
# increments of 24, 21, 29, and 25 to represent the 15 Minute Time
# Segments allocated to Night, Early Evening, Afteroon, and Morning
# Respectively (12 a.m. - 6 a.m, 7 p.m. - 12 a.m., 12 p.m. - 7 p.m.,
# annd ( 6 a.m. - 12 p.m. respectively). 
sumdata = 0
#The four variables below are used to hold the output from our
#Load Clustering Algorithm for each of the four chosen Segments of
# the Day.
morningdata = np.zeros((31))
afternoondata = np.zeros((31))
evening1data = np.zeros((31))
evening2data = np.zeros((31))

#LOAD CLUSTERING ALGORITHM/ANALYSIS

#Run through the Electricity Consumption Data for the Month
for j in range(0,31):
    #Run through the Electricity Consumption Data for Each Day
    for k in range(start,start+96):
        #Zero out the variable used to count Clustering Data for the Day Segment
        sumdata = 0
        #Run through the Electricity Consumption Data for the Night Segment
        # (12 a.m. - 6 a.m.)
        for m in range(start, start+23):
            # If the value of the Consumption Data is greater than the
            # Recorded Maximum Electricity Consumed by the User,
            # count it as a HIGH Consumption by the User
            if(januaryconsumption[m] >= 0.7 * maxconsumption):
                sumdata = sumdata + 1
            #If all the Electricity Consumption Data for the Evening Segment
            # are counted as HIGH, then the User has a HIGH Evening Segment
            # Consumption, and this recorded as a value 1 for the Segment.
            if(sumdata == 24):
                evening2data[j]= 1

        #Zero out the variable used to count Clustering Data for the Day Segment 
        sumdata = 0
        #Run through the Electricity Consumption Data for the Early Evening Segment        
        for m in range(start+75, start+95):
            # If the value of the Consumption Data is greater than the
            # Recorded Maximum Electricity Consumed by the User,
            # count it as a HIGH Consumption by the User
            if(januaryconsumption[m] >= 0.7 * maxconsumption):
                sumdata = sumdata + 1
            #If all the Electricity Consumption Data for the Early Evening Segment
            # are counted as HIGH, then the User has a HIGH Early Evening Segment
            # Consumption, and this recorded as a value 1 for the Segment.
                if(sumdata == 21):
                    evening1data[j]= 1
        #Zero out the variable used to count Clustering Data for the Day Segment
        sumdata = 0
        #Run through the Electricity Consumption Data for the Afternoon Segment
        for m in range(start+47, start+75):
            # If the value of the Consumption Data is greater than the
            # Recorded Maximum Electricity Consumed by the User,
            # count it as a HIGH Consumption by the User
            if(januaryconsumption[m] >= 0.7 * maxconsumption):
                sumdata = sumdata + 1
                #If all the Electricity Consumption Data for the Afternoon Segment
                # are counted as HIGH, then the User has a HIGH Afternoon Segment
                # Consumption, and this recorded as a value 1 for the Segment.
                if(sumdata == 31):
                    afternoondata[j]= 1        
        #Zero out the variable used to count Clustering Data for the Day Segment 
        sumdata = 0
        #Run through the Electricity Consumption Data for the Morning Segment
        for m in range(start+23, start+47):
            # If the value of the Consumption Data is greater than the
            # Recorded Maximum Electricity Consumed by the User,
            # count it as a HIGH Consumption by the User
            if(januaryconsumption[m] >= 0.7 * maxconsumption):
                sumdata = sumdata + 1
                #If all the Electricity Consumption Data for the Morning Segment
                # are counted as HIGH, then the User has a HIGH Morning Segment
                # Consumption, and this recorded as a value 1 for the Segment.               
                if(sumdata == 14):
                    morningdata[j]= 1
        
    
    # Increment Start Value to move on to the Next Day for Processing and Clustering
    start = start +96

#Print Results
print("Results")
print("Morning Data")
print(morningdata)
print("Afternoon Data")
print(afternoondata)
print("Evening 1 Data")
print(evening1data)
print("Evening 2 Data")
print(evening2data)

# The Customer Evening Data was clustered in 2 Sections (Early Evening Data and
# Night Data). So we need to group them together before we perform a Load Analysis
# on the Data
eveningdata = evening1data + evening2data
for j in range(0,31):
    if(eveningdata[j] == 1):
        eveningdata[j] = 0
    if(eveningdata[j] == 2):
        eveningdata[j] = 1

# For Each of the three Segments of the Day (Morning, Afternoon, and Evening), the
# Clustering Algorithm has classified the User Electricity Consumption as either a
# HIGH, which is a 1 value, or a LOW, which is a 0 value.
# We take the value with the highest freqency of occurence to be the actual
# representation of the User's Electricity Profile for that Segment,
# This is done by taking the modal value of the Load Clustering Profile obtained
# for the Three Electricity Segments of the Day (Morning, Afternoon, and Evening).
morningdata_mode = mode(morningdata)
afternoondata_mode = mode(afternoondata)
eveningdata_mode = mode(eveningdata)

#Print Modal Values of the Three Segments
print(morningdata_mode)
print(afternoondata_mode)
print(eveningdata_mode)


# LOAD PROFILE CLASSIFICATION

# GET USER LOAD PROFILE
# The Electricity Consumption Load Profiles that we have designed are as follows:
# 1. RESIDENTIAL:- ALL NIGHT HIGH CONSUMPTION
# 2. INUDSTIRAL/COMMERCIAL:- ALL DAY HIGH CONSUMPTION
# 3. MAXIMUM CONSUMER:- ALL DAY AND NIGHT HIGH CONSUMPTION (TRANSFORMATION SYSTEMS & SUBWAYS, POWER GENERATING SYSTEMS)
# 4. EARLY BIRD:- ALL MORNING HIGH (PEOPLE THAT WORK NIGHT HOURS AND SLEEP AT DAY)
# 5. HIGH PROFILE:- ALL FTERNOON HIGH - BUILDINGS THAT OPERATE WITH PHOTOVOLTAIC POWER SOURCES
# 6. MINIMUM CONSUMER:- STRAIGHT-LINE CONSUMER WITH LOW CONSUMPTION VALLUES
# 7. LOW PROFILE CONSUMER - NO HIGH CONSUMPTION


if((morningdata_mode == 0) & (afternoondata_mode == 0) & (eveningdata_mode == 0)):
    # If the User has consumed Low Electricty for the THREE (3) Segments of the Day for 31 Days, then:
    #USER IS LOW PROFILE CONSUMER
    LOADPROFILE = 7

if((morningdata_mode == 0) & (afternoondata_mode == 0) & (eveningdata_mode == 1)):
    # If the User has consumed High Electricty for the EVENING Segment of the Day ONLY, for 31 Days, then:
    #USER IS RESIDENTIAL
    LOADPROFILE = 1
    
if((morningdata_mode == 0) & (afternoondata_mode == 1) & (eveningdata_mode == 0)):
    # If the User has consumed High Electricty for the AFTERNOON Segments of the Day ONLY, for 31 Days, then:
    #USER IS HIGH ROFILE CONSUMER
    LOADPROFILE = 5

if((morningdata_mode == 1) & (afternoondata_mode == 1) & (eveningdata_mode == 0)):
    # If the User has consumed High Electricty for the MORNING and AFTERNOON Segments of the Day ONLY, for 31 Days, then:
    #USER IS INDUSTRIAL/COMMERCIAL
    LOADPROFILE = 2

if((morningdata_mode == 1) & (afternoondata_mode == 0) & (eveningdata_mode == 0)):
    # If the User has consumed High Electricty for the MORNING Segment of the Day ONLY, for 31 Days, then:
    #USER IS EARLY BIRD CONSUMER
    LOADPROFILE = 4


# Determine if the User is a Straight Line Conumer

#Obtain the difference between the User's Maximum Electricity Consumption and the User's Minimum Electricity
# Consumption.
straightlinetest = maxconsumption - minconsumption

if(straightlinetest <= 2):
    # USER HAS A STRAIGHT LINE PROFILE OR FLAT LINE IF MAX-MIN < 2KWH
    #SET USER AS MAXIMUM CONSUMER FIRST
    LOADPROFILE = 3
    if(maxconsumption < 2):
        #Check if the User is Minimum Consumer Instead.
        #USER IS A MINIMUM CONSUMER if MAX CONSUMPTION < 2KWH
        LOADPROFILE = 6

#(If (maxconsumption = minconsumption) <= a certain value
#    => straight line (flat line)
#   Set Consumer Profile = 3 (MAXIMUM CONSUMER)
#   If (maxconsumption <= certain value)
#    => Set Profile 6 (MINIMUM CONSUMER)


# PRINT CLUSTERED LOAD PROFILE FOR THE USER
print("FINAL LOAD PROFILE FOR USER:")
print(LOADPROFILE)
y2 = [0,0,0,0,0]
CHARTTITLE = ""
LOADPROFILE_STRING = ["RESIDENTIAL CONSUMER", "INDUSTRIAL/COMMERCIAL CONSUMER", "MAXIMUM CONSUMER", "EARLY BIRD CONSUMER", "HIGH PROFILE CONSUMER", "MINIMUM CONSUMER", "LOW PROFILE CONSUMER" ]

if(LOADPROFILE == 1):
    print(LOADPROFILE_STRING[0])
    #Set Chart Title for Load Display
    CHARTTITLE = LOADPROFILE_STRING[0]
    # Set Data for Clustered Load Profile Display for 31 Days
    y2 = [maxconsumption,((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2),maxconsumption,maxconsumption]
if(LOADPROFILE == 2):
    print(LOADPROFILE_STRING[1])
    #Set Chart Title for Load Display    
    CHARTTITLE = LOADPROFILE_STRING[1]
    # Set Data for Clustered Load Profile Display for 31 Days
    y2 = [((maxconsumption-minconsumption)/2),maxconsumption,maxconsumption,((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2)]
if(LOADPROFILE == 3):
    print(LOADPROFILE_STRING[2])
    #Set Chart Title for Load Display
    CHARTTITLE = LOADPROFILE_STRING[2]
    # Set Data for Clustered Load Profile Display for 31 Days
    y2 = [maxconsumption,maxconsumption,maxconsumption,maxconsumption,maxconsumption]
if(LOADPROFILE == 4):
    print(LOADPROFILE_STRING[3])
    #Set Chart Title for Load Display
    CHARTTITLE = LOADPROFILE_STRING[3]
    # Set Data for Clustered Load Profile Display for 31 Days
    y2 = [((maxconsumption-minconsumption)/2),maxconsumption,((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2)]
if(LOADPROFILE == 5):
    print(LOADPROFILE_STRING[4])
    #Set Chart Title for Load Display
    CHARTTITLE = LOADPROFILE_STRING[4]
    # Set Data for Clustered Load Profile Display for 31 Days
    y2 = [((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2),maxconsumption,((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2)]
if(LOADPROFILE == 6):
    print(LOADPROFILE_STRING[5])
    #Set Chart Title for Load Display
    CHARTTITLE = LOADPROFILE_STRING[5]
    # Set Data for Clustered Load Profile Display for 31 Days
    y2 = [maxconsumption,maxconsumption,maxconsumption,maxconsumption,maxconsumption]
if(LOADPROFILE == 7):
    print(LOADPROFILE_STRING[6])
    #Set Chart Title for Load Display
    CHARTTITLE = LOADPROFILE_STRING[6]
    # Set Data for Clustered Load Profile Display for 31 Days
    y2 = [((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2),((maxconsumption-minconsumption)/2)]


# DISPLAY LOAD PROFILE DATA AND CLUSTERING LOAD PROFILE, AND DEMAND RESPONSE PROGRAMS
#Plot Lomded User Profile to see

#Variable to hold time count for the 15 Minute Segments of Each Day for 31 Days Data
xaxis = range(2975)
#Obtin mean Consumption of the 31 Days Data
consumption_mean = mean(januaryconsumption)

#Plot the Mean Consumption of the User's Electricity Profile for 31 Days.
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


#Varialbe to hold time count for 31 Days, 1 count per day
xaxis2= range(30)

#Variable to hold the values to plot the Four Segmens of the Day (Morning, Afternoon,
# Early Evening, and Night) on the X axis. Y axis values have been identified above.
x2= [0,23,47,75, 95]
#Plot the LOAD PROFILE OF THE USER'S ELECTRICITY DATA FOR THE GIVEN MONTH
plt.plot(x2, y2, label = CHARTTITLE + " LOAD PROFILE", color='blue', linewidth = 6)
plt.xlim(0,24)
plt.xlabel('Time in 15 MINUTE SEGMENTS for ONE FULL DAY')
plt.ylabel('ELECTRICITY CONSUMED (KWh)')
plt.title(CHARTTITLE + " LOAD PROFILE") 
# show a legend on the plot
plt.legend()
plt.show()

# Plot Consumer Load Profile Using Pie Chart
# Variables to Hold Segments of the Day
activities = ['Morning', 'Afternoon', 'Evening', 'Night']

# Section of the Pie Chart (24) that is allocated to each of the four (4)
# Segments of the Day (Morning, Afternoon, Early Evening, and Night).
slices = [6, 7, 5, 6]
 
# Color Code for each label
# Red indicates that the Electriicty Consumption in a Section of the Day Segment is HIGH
# Blue indicates that the Electricity Consumption in a Section of the Day Segment is LOW
colors = ['b', 'b', 'r', 'r']
if(LOADPROFILE == 1):
    colors = ['b', 'b', 'r', 'r']
if(LOADPROFILE == 2):
    colors = ['r', 'r', 'b', 'b']
if(LOADPROFILE == 3):
    colors = ['r', 'r', 'r', 'r']
if(LOADPROFILE == 4):
    colors = ['r', 'b', 'b', 'b']
if(LOADPROFILE == 5):
    colors = ['b', 'r', 'b', 'b']
if(LOADPROFILE == 6):
    colors = ['b', 'b', 'b', 'b']
if(LOADPROFILE == 7):
    colors = ['b', 'b', 'b', 'b']

# PLOT THE LOAD CLUSTERED PIE CHART OF THE USER
plt.pie(slices, labels = activities, colors=colors, 
        startangle=90, shadow = True, explode = (0, 0, 0.1, 0),
        radius = 1.2, autopct = '%1.1f%%')
plt.title(CHARTTITLE + " LOAD PROFILE")
# plotting legend
plt.legend() 
# showing the plot
plt.show()


#DEMAND RESPONSE PROGRAM

#Open window to display the Demand Response Program for the User Load Profile that
# has been correctly identified and clustered by the ALGORITHM
mainwindow = tk.Tk()
mainwindow.geometry("1400x700")
mainwindow.title('DEMAND RESPONSE PROGRAM BY OLAWUYI RACETT NIGERIA LTD., WELLINGTON SQUARE, OXFORD, OX1 2JD, LONDON, UNITED KINGDOM RC14668218')
mainwindow['background']='#7F7FFF'
mainwindow.iconbitmap('companylogo.ico')

#Insert OX12JD COMPANY LOGO AND EL ELYON
# Create a canvas widget
canvas=Canvas(mainwindow, width=1400, height=100)
canvas.pack()

#Upload Images
img=ImageTk.PhotoImage(file="LOGO3.png")
img3=ImageTk.PhotoImage(file="UKFLAG.png")
img4=ImageTk.PhotoImage(file="UKMAP.jpeg")
img5=ImageTk.PhotoImage(file="MEDSOFTWAREUKN BACKGROUND4.png")
img6=ImageTk.PhotoImage(file="MEDSOFTWAREUKN BACKGROUND5.png")
img7=ImageTk.PhotoImage(file="ISHI.png")

canvas.create_image(200, 50, image=img3)
canvas.create_image(1235, 50, image=img4)
canvas.create_image(680, 50, image=img6)

#Insert OX12JD COMPANY HEADING
label2 = tk.Label(text="DEMAND RESPONSE PROGRAM FOR ELECTRICITY CONSUMERS", width=65, height=1, font=('Monotype Corsiva', 18), bg='#ffffff') 
label2.place(x=260,y=15)

#Set String for Visual Display
if(LOADPROFILE == 1):
    DPR = "RESIDENTIAL PROGRAM"
    img8=ImageTk.PhotoImage(file="RESIDENTIALCONSUMER.png")
if(LOADPROFILE == 2):
    DPR = "INDUSTRIAL/COMERCIAL PROGRAM"
    img8=ImageTk.PhotoImage(file="INDUSTRIALCONSUMER.png")
if(LOADPROFILE == 3):
    DPR = "MAXIMUM CONSUMER PROGRAM"
    img8=ImageTk.PhotoImage(file="MAXIMUMCONSUMER.png")
if(LOADPROFILE == 4):
    DPR = "EARLY BIRD PROGRAM"
    img8=ImageTk.PhotoImage(file="EARLYBIRDCONSUMER.png")
if(LOADPROFILE == 5):
    DPR = "HIGH PROFIELE PROGRAM"
    img8=ImageTk.PhotoImage(file="HIGHPROFILECONSUMER.png")
if(LOADPROFILE == 6):
    DPR = "MINIMUM CONSUMER PROGRAM"
    img8=ImageTk.PhotoImage(file="MINIMUMCONSUMER.png")
if(LOADPROFILE == 7):
    DPR = "LOW PROFILE CONSUMER PROGRAM"
    img8=ImageTk.PhotoImage(file="LOWPROFILECONSUMER.png")
    
label3 = tk.Label(text=DPR, width=48, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
label3.place(x=320,y=60)

#ADD CLUSTERED CONSUMER LOAD PROFILE IMAGE
canvas3=Canvas(mainwindow, width=600, height=600)
canvas3.place(x=1,y=100)
canvas3.create_image(300, 300, image=img8)

#Display Demand Response Program for the User
if(LOADPROFILE == 1):
    label4 = tk.Label(text="Residential Consumers are Citizens who consume Maximum Electricity ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label4.place(x=640,y=115)
    label5 = tk.Label(text=" during the night hours (7 p.m.- 6 a.m.). ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label5.place(x=640,y=150)
    label6 = tk.Label(text="These citizens should be given a card or a device that will enable them ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label6.place(x=640,y=190)
    label7 = tk.Label(text="to report in the morning, the amount of electricity they would consume ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label7.place(x=640,y=225)
    label8 = tk.Label(text="at night for that specific day, and this should be done daily,", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label8.place(x=640,y=260)
    label9 = tk.Label(text="to enable the grid management system provide sufficient electricity ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label9.place(x=640,y=295)
    label10 = tk.Label(text="for them each day.", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label10.place(x=640,y=330)

if(LOADPROFILE == 2):
    label4 = tk.Label(text="Industrial Consumers are Citizens who consume Maximum Electricity ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label4.place(x=640,y=115)
    label5 = tk.Label(text=" during the daylight hours (6 a.m.- 7 p.m.). ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label5.place(x=640,y=150)
    label6 = tk.Label(text="These citizens should be given an incentive to reduce their ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label6.place(x=640,y=190)
    label7 = tk.Label(text="Electricity Consumption during the night hours down to zero(0). ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label7.place(x=640,y=225)
    label8 = tk.Label(text="This program is called the Zero-Down Program. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label8.place(x=640,y=260)
    label10 = tk.Label(text="For each month a citizen enrolled in this Program is able to cut down ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label10.place(x=640,y=295)
    label11 = tk.Label(text="their night time electricity consumption down to zero, ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label11.place(x=640,y=330)
    label12 = tk.Label(text="He or She is given half-off their electricity bill for the following month. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label12.place(x=640,y=365)
     
  
if(LOADPROFILE == 6):
    label4 = tk.Label(text="Minimum Consumers are Citizens who consume Minimum Electricity ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label4.place(x=640,y=115)
    label5 = tk.Label(text=" throughout the month, such that they have a Straight-Line Profile ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label5.place(x=640,y=150)
    label6 = tk.Label(text="with their electricity consumption falling below 2 Kwh per 15", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label6.place(x=640,y=185)
    label7 = tk.Label(text="Minute Segement of consumption. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label7.place(x=640,y=220)
    label8 = tk.Label(text="These citizens should be rewarded with an Education Savings Dividend ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label8.place(x=640,y=260)
    label10 = tk.Label(text="or Payout from a Taxable Edcucation Savings Scheme run by the ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label10.place(x=640,y=295)
    label11 = tk.Label(text="Electricity Distribution Network. The final amount for the Education ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label11.place(x=640,y=330)
    label12 = tk.Label(text="Savings Dividend paid out to the Minimum Consumer for that ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label12.place(x=640,y=365)
    label13 = tk.Label(text="specific month is determined by the value of the Electricity Consumed ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label13.place(x=640,y=400)
    label14 = tk.Label(text="subtracted from the 2KWh per 15 Minute consumption segment, ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label14.place(x=640,y=435)
    label15 = tk.Label(text="multiplied by a fixed rate. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label15.place(x=640,y=470)    
  

if(LOADPROFILE == 4):
    label4 = tk.Label(text="Early Bird Consumers are Citizens who consume Maximum Electricity ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label4.place(x=640,y=115)
    label5 = tk.Label(text=" during the Morning Hours (6 a.m.- 7 p.m.). ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label5.place(x=640,y=150)
    label6 = tk.Label(text="These citizens should be given a 20% write off ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label6.place(x=640,y=190)
    label7 = tk.Label(text="for their Electricity bill for the month as a reward ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label7.place(x=640,y=225)
    label8 = tk.Label(text="for Low Energy Consumption in the other three segments ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label8.place(x=640,y=260)
    label9 = tk.Label(text="of the day (Afternoon, Early Evening, and Night). ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label9.place(x=640,y=295)


if(LOADPROFILE == 5):
    label4 = tk.Label(text="High Profile Consumers are Citizens who consume Maximum Electricity ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label4.place(x=640,y=115)
    label5 = tk.Label(text=" during the Afternoon Hours (12 p.m.- 7 p.m.). ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label5.place(x=640,y=150)
    label6 = tk.Label(text="These citizens should be flagged for integration into ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label6.place(x=640,y=190)
    label7 = tk.Label(text="Solar Power Tower Sources. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label7.place(x=640,y=225)
    label8 = tk.Label(text="This is because they would be the easiest set of consumers to be readily ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label8.place(x=640,y=260)
    label9 = tk.Label(text="integrated into renewable energy sources from Solar Energy, because ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label9.place(x=640,y=295)
    label10 = tk.Label(text="majority of their energy consumption is done during the afternoon hours. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label10.place(x=640,y=330)
    label1 = tk.Label(text="There should also be incentives given to Citizens in the ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label1.place(x=640,y=365)
    label2 = tk.Label(text="High Profile Program for being the first set of consumers ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label2.place(x=640,y=400)
    label3 = tk.Label(text="to be completely converted to purely renewable energy source Consumers. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label3.place(x=640,y=435)
    label4 = tk.Label(text="The incentive should be a tax write off for contributing to ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label4.place(x=640,y=470)
    label5 = tk.Label(text="the reduction of CO2 Emissions by utilizing only ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label5.place(x=640,y=505)
    label6 = tk.Label(text="Solar Power Generation for Electricity Consumption. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label6.place(x=640,y=540)


if(LOADPROFILE == 3):
    label4 = tk.Label(text="Maximum Consumers are Citizens who consume Maximum Electricity ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label4.place(x=640,y=115)
    label5 = tk.Label(text=" throughout the month, such that they have a Straight-Line Profile ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label5.place(x=640,y=150)
    label6 = tk.Label(text="with their electricity consumption falling above 4 Kwh per 15", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label6.place(x=640,y=185)
    label7 = tk.Label(text="Minute Segement of consumption. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label7.place(x=640,y=220)
    label8 = tk.Label(text="These citizens should be regarded as Tier 1 customers and given ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label8.place(x=640,y=260)
    label9 = tk.Label(text="preferential treatment by the Electricity Company because: ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label9.place(x=640,y=295)
    label10 = tk.Label(text="1. They provide Exhorbitant & Steady income for it, ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label10.place(x=640,y=330)
    label12 = tk.Label(text="regardless of what electricity tarriffs they are charged. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label12.place(x=640,y=365)
    label13 = tk.Label(text="2. Their Electricity Demand remains constantly high, Day, Month, ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label13.place(x=640,y=400)
    label14 = tk.Label(text="& Year, so they are Reliable Customers for the Electricity Company. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label14.place(x=640,y=435)
    label16 = tk.Label(text="To this effect, we have designed TWO (2) Perks for Consumers in the ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label16.place(x=640,y=470)
    label17 = tk.Label(text="Maximum Consumer Program: ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label17.place(x=640,y=505)
    label18 = tk.Label(text="1. Direct Connection to a Dedicated Personal PowerPlant, so as to ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label18.place(x=640,y=540)
    label19 = tk.Label(text="ensure their Electricity Needs are Met. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label19.place(x=640,y=575)
    label20 = tk.Label(text="2. Personal Yearly Visits to determine their Projected Electricity Needs ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label20.place(x=640,y=610)
    label21 = tk.Label(text=" and to make Adequate Plans to Satisfy them. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label21.place(x=640,y=645)

if(LOADPROFILE == 7):
    label4 = tk.Label(text="Low Profile Consumers are Citizens who consume Minimum Electricity ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label4.place(x=640,y=115)
    label5 = tk.Label(text=" throughout the Day (Morning, Afternoon, Early Evening, ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label5.place(x=640,y=150)
    label6 = tk.Label(text="and Night Hours).", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label6.place(x=640,y=185)
    label7 = tk.Label(text="Their Electricity Projection Needs are already identified. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label7.place(x=640,y=225)
    label8 = tk.Label(text="Because they consume low electricity at all four segments of the day, ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label8.place(x=640,y=260)
    label10 = tk.Label(text="This implies that their demand for electricity falls below 70% of ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label10.place(x=640,y=295)
    label11 = tk.Label(text="their maximum demand for electricity. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label11.place(x=640,y=330)
    label12 = tk.Label(text="Therefore, for citizens in the Low Profile Consumer Program, ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label12.place(x=640,y=365)
    label13 = tk.Label(text="The Electricity Company can make provisions to supply them with ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label13.place(x=640,y=400)
    label14 = tk.Label(text="their projected demand by simply providing them with 70% ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label14.place(x=640,y=435)
    label15 = tk.Label(text="of their recorded maximum demand for electricity. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label15.place(x=640,y=470)    
    label16 = tk.Label(text="In this way, the Electricity Grid is freed up to provide ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label16.place(x=640,y=505)    
    label17 = tk.Label(text="the rest of the Available Electricity to citizens in the ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label17.place(x=640,y=540)    
    label18 = tk.Label(text="Other Consumer Programs, such as ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label18.place(x=640,y=575)
    label19 = tk.Label(text="The Residential and Industrial Consumers. ", width=50, height=1, font=('Monotype Corsiva', 20), bg='#ffffff') 
    label19.place(x=640,y=610) 
 



