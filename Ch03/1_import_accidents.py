import sqlite3 # provides python with a library for sqlite
import csv # used to import csv file
import urllib.request # used to download a copy of data

SQLITE_FILE = "UKRoadData.sqlite"

# opens sqlite and a database file
conn = sqlite3.connect(SQLITE_FILE)

# provides a connection to the database
myCursor = conn.cursor()

# create the table we'll import data into
# Handling the CREATE string this way is somewhat inelegant. There are better ways to do this
# and we'll explore them in the next step
do_this_sqlite = '''
CREATE TABLE `Accidents_2015` (
	`Accident_Index`,
	`Location_Easting_OSGR`,
	`Location_Northing_OSGR`,
	`Longitude`,
	`Latitude`,
	`Police_Force`,
	`Accident_Severity`,
	`Number_of_Vehicles`,
	`Number_of_Casualties`,
	`Date`,
	`Day_of_Week`,
	`Time`,
	`Local_Authority_(District)`,
	`Local_Authority_(Highway)`,
	`1st_Road_Class`,
	`1st_Road_Number`,
	`Road_Type`,
	`Speed_limit`,
	`Junction_Detail`,
	`Junction_Control`,
	`2nd_Road_Class`,
	`2nd_Road_Number`,
	`Pedestrian_Crossing-Human_Control`,
	`Pedestrian_Crossing-Physical_Facilities`,
	`Light_Conditions`,
	`Weather_Conditions`,
	`Road_Surface_Conditions`,
	`Special_Conditions_at_Site`,
	`Carriageway_Hazards`,
	`Urban_or_Rural_Area`,
	`Did_Police_Officer_Attend_Scene_of_Accident`,
	`LSOA_of_Accident_Location`
);
 '''
myCursor.execute(do_this_sqlite) # creates an empty table

# this next set of commands populates that table

# import the accident data
AccidentsLocation = "https://data.yorkopendata.org/dataset/c0eec478-ef19-4234-826f-8efb9563eda2/resource/aa8bcb3d-3945-4347-adc9-24d8e1d3e05c/download/accidents.csv"
urllib.request.urlretrieve(AccidentsLocation, 'Accidents_2015.csv')

reader = csv.reader(open('Accidents_2015.csv', 'r'), delimiter=',')

rowIDCount = 0 # used to strip out the first line of csv

for row in reader:
    if rowIDCount:
        row = [ x.strip() for x in row ] # trim whitespace from front and end of string
        myCursor.execute("INSERT INTO Accidents_2015 (`Accident_Index`,`Location_Easting_OSGR`,`Location_Northing_OSGR`,`Longitude`,`Latitude`,`Police_Force`,`Accident_Severity`,`Number_of_Vehicles`,`Number_of_Casualties`,`Date`,`Day_of_Week`,`Time`,`Local_Authority_(District)`,`Local_Authority_(Highway)`,`1st_Road_Class`,`1st_Road_Number`,`Road_Type`,`Speed_limit`,`Junction_Detail`,`Junction_Control`,`2nd_Road_Class`,`2nd_Road_Number`,`Pedestrian_Crossing-Human_Control`,`Pedestrian_Crossing-Physical_Facilities`,`Light_Conditions`,`Weather_Conditions`,`Road_Surface_Conditions`,`Special_Conditions_at_Site`,`Carriageway_Hazards`,`Urban_or_Rural_Area`,`Did_Police_Officer_Attend_Scene_of_Accident`,`LSOA_of_Accident_Location`) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", row)
    rowIDCount += 1

conn.commit()
