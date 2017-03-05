#!/bin/env python2.7

import sqlite3 # provides python with a library for sqlite
import csv # used to import Cal Enviro Screen csv file

conn = sqlite3.connect("calEnviro.sqlite") # opens sqlite and a database file

myCursor = conn.cursor() # provides a connection to the database

# create the table we'll import data into
# Handling the CREATE string this way is somewhat inelegant. There are better ways to do this
# for example, use a dictionary to store the field names and types. This would allow for reuse in the "insert" segment
myCursor.execute('CREATE TABLE CalEnviro("Census Tract" INTEGER,"Total Population" INTEGER,"California County" TEXT,"Click for interactive map" NULL,"CES 2.0 Score" REAL,"CES 2.0 Percentile Range" REAL,"Hyperlink" REAL,"Ozone" REAL,"Ozone Pctl" REAL,"PM2.5" REAL,"PM2.5 Pctl" REAL,"Diesel PM" REAL,"Diesel PM Pctl" REAL,"Drinking Water" REAL,"Drinking Water Pctl" REAL,"Pesticides" REAL,"Pesticides Pctl" REAL,"Tox. Release" REAL,"Tox. Release Pctl" REAL,"Traffic" REAL,"Traffic Pctl" REAL,"Cleanup Sites" REAL,"Cleanup Sites Pctl" REAL,"Groundwater Threats" REAL,"Groundwater Threats Pctl" REAL,"Haz. Waste" REAL,"Haz. Waste Pctl" REAL,"Imp. Water Bodies" REAL,"Imp. Water Bodies Pctl" REAL,"Solid Waste" REAL,"Solid Waste Pctl" REAL,"Pollution Burden" REAL,"Pollution Burden Score" REAL,"Pollution Burden Pctl" REAL,"Age" REAL,"Age Pctl" REAL,"Asthma" REAL,"Asthma Pctl" REAL,"Low Birth Weight" REAL,"Low Birth Weight Pctl" REAL,"Education" REAL,"Education Pctl" REAL,"Linguistic Isolation" REAL,"Linguistic Isolation Pctl" REAL,"Poverty" REAL,"Poverty Pctl" REAL,"Unemployment" REAL,"Unemployment Pctl" REAL,"Pop. Char. " REAL,"Pop. Char. Score" REAL,"Pop. Char. Pctl" REAL,"Location 1" TEXT);')

reader = csv.reader(open('CalEnviroScreen_2.0_2014.csv', 'r'), delimiter=',')

rowIDCount = 0 # used to strip out the first line of csv

for row in reader:
    if rowIDCount:
        row = [ x.strip() for x in row ] # trim whitespace from front and end of string
        myCursor.execute('INSERT INTO CalEnviro ("Census Tract","Total Population" ,"California County" ,"Click for interactive map" ,"CES 2.0 Score" ,"CES 2.0 Percentile Range" ,"Hyperlink" ,"Ozone" ,"Ozone Pctl" ,"PM2.5" ,"PM2.5 Pctl" ,"Diesel PM" ,"Diesel PM Pctl" ,"Drinking Water" ,"Drinking Water Pctl" ,"Pesticides" ,"Pesticides Pctl" ,"Tox. Release" ,"Tox. Release Pctl" ,"Traffic" ,"Traffic Pctl" ,"Cleanup Sites" ,"Cleanup Sites Pctl" ,"Groundwater Threats" ,"Groundwater Threats Pctl" ,"Haz. Waste" ,"Haz. Waste Pctl" ,"Imp. Water Bodies" ,"Imp. Water Bodies Pctl" ,"Solid Waste" ,"Solid Waste Pctl" ,"Pollution Burden" ,"Pollution Burden Score" ,"Pollution Burden Pctl" ,"Age" ,"Age Pctl" ,"Asthma" ,"Asthma Pctl" ,"Low Birth Weight" ,"Low Birth Weight Pctl" ,"Education" ,"Education Pctl" ,"Linguistic Isolation" ,"Linguistic Isolation Pctl" ,"Poverty" ,"Poverty Pctl" ,"Unemployment" ,"Unemployment Pctl" ,"Pop. Char. " ,"Pop. Char. Score" ,"Pop. Char. Pctl" ,"Location 1") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);', row)
    rowIDCount += 1

conn.commit()
