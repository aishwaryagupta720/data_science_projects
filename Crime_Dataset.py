# Import the required modules in this cell
import pandas as pd
import datetime as dt
import reverse_geocoder as rg 
import pprint
import re
from google.colab import drive
drive.mount("/content/drive")
# We will reference this dataframe as "Main Dataframe"

df = pd.read_csv("Assignment_Crime_Data_from_2010_to_Present.csv")
df.head()
### Question 1 : Use any 5 pandas attributes to understand the DataFrame structure and metadata.
list(df.head().index)
print("Geenral Info: ",df.info)
print("Column Values: ",df.columns)
print("Index Range: ",df.index)
print("Datatypes in DF: ",df.dtypes)
print("Dimensions of DataFrame: ",df.shape)
print("Size of DataFrame",df.size)
rows=len(df.axes[0])
cols=len(df.axes[1])
print("Number of rows:",rows," and Number of Columns:",cols)

### Question 2: Create another blank DataFrame and insert the data from this sheet --> Python Assignment.xlsx(Present in the same drive folder) And append this new dataframe to the main dataframe . (Hint Check the structure after appending the DataFrame)
# Write answer here
print("Shape of Main DataFrame before appending: ",len(df.axes[0]))
df_side=pd.read_excel("Python Assignment.xlsx")
print("Shape of Side DataFrame: ",len(df_side.axes[0]))

# print(df.dtypes)
# print(df_side.dtypes)

df_main=df.append(df_side,ignore_index=True,verify_integrity=True)

# print(df_main.dtypes)

# Datetime formats were inconsistent
dt_format='%d/%m/%Y'
#convert to datetime datatype then make format consistent
df_main['Date Occurred'] = pd.to_datetime(df_main['Date Occurred']).dt.strftime(dt_format)
df_main['Date Reported'] = pd.to_datetime(df_main['Date Reported']).dt.strftime(dt_format)



print("Shape of Main DataFrame after appending: ",len(df_main.axes[0]))
### Question 3.a : Find the area where maximum crimes were committed?
# Write answer here
area=df_main.groupby("Area Name").count().Address
# Grouped by Area name
# Counted the number of occurances of each( can find mean/median/etc). 
# only display count of one column(arbitrary)
area=area.idxmax()
print("Area with Most crime Occurances: ",area)
# return first occurance of maximum idxmax()

### Question 3.b : Find the average age of the victims?
# Write answer here
tdf=df_main[(df_main['Area Name']==area)]
age=tdf['Victim Age'].mean()
print("the average age of the victims: ",age)


### Question 4 : Which type of crime was the 5th most reported crime where the victim age is greater then 40 years?
# Write answer here
temp=df_main[(df_main['Victim Age'] >40)]
# Filter df_main by (Victim age>40)

series=temp.groupby('Crime Code Description').count().Address
# Grouped by Crime Code Description (as its value is important for end result)
# Counted the number of occurances of each( can find mean/median/etc). 
# only display count of one column(arbitrary)

series=series.nlargest(5)
# Find top 5 values based on count nlargest(5)

print("5th most reported crime where the victim age is greater then 40 years:\n",series.tail(1).index[0])
# last value in top 5 (5th largest)

###Question 5 : Find the month and the year in which most of the crimes were reported?
# Write answer here

date=df_main.groupby("Date Reported").count().Address
# Grouped by Date
# Counted the number of occurances of each( can find mean/median/etc). 
# only display count of one column(arbitrary)

date=date.idxmax()
#get max value from series 

#format saved while appending
date= dt.datetime.strptime(date, dt_format)

print("Most crime Occurances:\nMonth: ",date.month,"Year: ",date.year)

###Question 6 : Which weapon was used the second most no of times to commit the crime in each area?

# Write answer here
temp=df_main.sort_values('Area Name')

area=set(temp['Area Name'].to_list())
area=list(area)

for a in area:
  # for every area 
  tdf=temp[(temp['Area Name']==a)]

  #group by weapons and count rows for each
  weapon=tdf.groupby("Weapon Description").count().Address
  
  # find top 2
  weapon=weapon.nlargest(2)

  #print second 
  print("Area:",a,"  Weapon :",weapon.tail(1).index[0])


### Question 7 : Find the full address where maximum crimes were committed (Hint use the location coordinates)?

# Write answer here

area=df_main.groupby("Location").count().Address
area=area.idxmax()

# extracting floating point numbers from string 
area = re.findall(r"[-+]?\d*\.\d+|\d+", area)

#using reverse-geocoder library
result = rg.search(area) 
pprint.pprint(result)   

# Question 8 : Find that hour of the day in which most of the crimes were committed
# Write answer here
time=df_main.groupby("Time Occurred").count().Address
time=time.idxmax()
print("hour of the day in which most of the crimes were committed: ",time)

# Question 9 : For each premise find out the gender that was more victimized?
# Write answer here
gender=df_main.groupby("Victim Sex").count().Address
gender=gender.idxmax()
print("Gender that was more victimized: ",gender)

# Question 10 : Within each area find for which Ethnic Groups were the most number of crimes committed the year 2015? Hint(Use the Victim Descent tab in this sheet https://colab.research.google.com/corgiredirector?site=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2F1RNx-Pt-rN5BNS31kkN2bcRg6HAcjhxdvw7rKqu2aoIQ%2Fedit%23gid%3D444749830 ) 
# Write answer here
d1 = dt.datetime(2014, 12, 21)
d2 = dt.datetime(2016, 1, 1)
df_main.dtypes 

# Filtering for dates greater than 12/12/2014
#converting to datetime type then comparing
tdf=df_main[(pd.to_datetime(df_main['Date Occurred'])>d1)]
#Filtering further for dates less than 1/1/2016
tdf=tdf[(pd.to_datetime(tdf['Date Occurred'])<d2 )]

area=set(tdf['Area Name'].to_list())
area=list(area) 

for a in area:
  # for every area 
  tdf=temp[(temp['Area Name']==a)]
  
  #group by Victim Descent
  ethnicity=tdf.groupby("Victim Descent").count().Address
  # find Descent with max crimes commited against
  ethnicity=ethnicity.idxmax()

  print("Area:",a,"  Victim Descent :",ethnicity)
