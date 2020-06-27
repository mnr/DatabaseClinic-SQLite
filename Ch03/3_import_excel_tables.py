
# import the two lookup tables from the excel file
# This requires xlrd.
# 1) open terminal
# 2) pip install xlrd
# if you get "ImportError", pip install -U pip setuptools then repeat

import sqlite3 # provides python with a library for sqlite
import xlrd
import urllib.request # used to download a copy of data


SQLITE_FILE = "UKRoadData.sqlite"
# opens sqlite and a database file
conn = sqlite3.connect(SQLITE_FILE)

# provides a connection to the database
myCursor = conn.cursor()


dataGuideURL = "http://data.dft.gov.uk/road-accidents-safety-data/variable%20lookup.xls"
urllib.request.urlretrieve(dataGuideURL, 'Road-Accident-Safety-Data-Guide.xls')

# open "Road-Accident-Safety-Data-Guide.xls"
roadDataXLS = xlrd.open_workbook(filename="Road-Accident-Safety-Data-Guide.xls")

##########################
# load the accident severity into the database
myCursor.execute("CREATE TABLE `accident_severity` ('Code','Label')")

accidentRows = roadDataXLS.sheet_by_name("Accident Severity").get_rows()
for arow in accidentRows:
    if arow[0].value == "code": continue
    theValues = (int(arow[0].value),arow[1].value)
    myCursor.execute("INSERT INTO 'accident_severity' VALUES (?,?) ",theValues)

##########################
# load the vehicle type into the database
myCursor.execute("CREATE TABLE `vehicle_type` ('Code','Label')")

accidentRows = roadDataXLS.sheet_by_name("Vehicle Type").get_rows()
for arow in accidentRows:
    if arow[0].value == "code": continue
    theValues = (int(arow[0].value),arow[1].value)
    myCursor.execute("INSERT INTO 'vehicle_type' VALUES (?,?) ",theValues)

conn.commit()
