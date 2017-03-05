#!/bin/env python2.7

import sqlite3 # provides python with a library for sqlite
import csv # used to import Cal Enviro Screen csv file

conn = sqlite3.connect("calEnviro.sqlite") # opens sqlite and a database file

myCursor = conn.cursor() # provides a connection to the database

# create a new population projections table

# create a list of tuples representing the data set
# Note: python dictionaries do not guarantee any order. Use a list instead
table_pop_proj = [["County Code", "INTEGER"],
  ["County Name", "TEXT"],
  ["Year", "TEXT"],
  ["Race Code", "REAL"],
  ["Race Name", "TEXT"],
  ["Gender", "TEXT"],
  ["Age", "INTEGER"],
  ["Population", "INTEGER"]
    ]

tempTableCreate = "" # a variable to build the create table

for afield in table_pop_proj:
    tempTableCreate += '"' + afield[0] + '" ' + afield[1] + ', '

tempTableCreate = tempTableCreate[:-2]

# tempTableCreate now contains the string needed to create the table

myCursor.execute('CREATE TABLE CA_PopulationProj (' + tempTableCreate + ');' )

# calEnviro.sqlite now contains an additional table (CA_PopulationProj)
# but...that table is empty. Now we need to import the data

# insertString will be used to create the SQL insert
# created this way, it will always match the table_pop_proj dictionary
insertString = "INSERT INTO CA_PopulationProj ("

for afield in table_pop_proj:
    insertString += '"' + afield[0] + '",'

insertString = insertString[:-1]

insertString += ") VALUES ("

insertString += "?," * len(table_pop_proj)

insertString = insertString[:-1]

insertString += ")"

# insertString now contains a properly constructed SQL insert call

with open('pop_proj.csv', 'rb') as csvfile:
    pproj_reader = csv.reader(csvfile)
    for row in pproj_reader:
        row = [ x.strip() for x in row ] # trim whitespace from front and end of string
        myCursor.execute(insertString, row) # insert that row into table

myCursor.execute('Delete from CA_PopulationProj Where RowID = 1 ;')

conn.commit()



