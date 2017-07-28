#!/bin/env python2.7

# import the vehicle data

import sqlite3 # provides python with a library for sqlite
import csv

SQLITE_FILE = "UKRoadData.sqlite"

conn = sqlite3.connect(SQLITE_FILE) # opens sqlite and a database file

myCursor = conn.cursor() # provides a connection to the database

# first, build the table
# use csv.reader (an iterator) to get the first line of the csv file
# (which we assume is column headers)
reader = csv.reader(open('Vehicles_2015.csv', 'r'), delimiter=',')
headers = reader.next()

# build the table from the csv headers
do_this_sqlite_1 = "CREATE TABLE `Vehicles_2015` ( "

for headerName in headers:
    do_this_sqlite_1 += "'" + headerName + "',"

# remove last comma
do_this_sqlite_1 = do_this_sqlite_1[:-1]

do_this_sqlite_1 += ");"
myCursor.execute(do_this_sqlite_1)

# then insert all of the data from the csv
# first, build an SQL command. ??? will be substituted for values by execute
do_this_sqlite = "INSERT INTO `Vehicles_2015` VALUES ( "
do_this_sqlite += "?," * len(headers) # are preferred to avoid sql injection
do_this_sqlite = do_this_sqlite[:-1]
do_this_sqlite += ")"

# reader is an iterator. reader.next() was the first row, so we start with the 2nd row
for row in reader:
    myCursor.execute(do_this_sqlite,row)

conn.commit()
