#!/bin/env python2.7

"""
For each line in the Shakespeare text,
CREATE a corresponding record in the database.
Each record will include the name of the character speaking,
the (absolute) line number of the phrase and the phrase itself,
trimmed of any leading or following spaces
"""

import sqlite3 # provides python with a library for sqlite
import time

conn = sqlite3.connect("shakespeare.sqlite") # opens sqlite and a database file

myCursor = conn.cursor() # provides a connection to the database

# create the table we'll import data into
# Handling the CREATE string this way is somewhat inelegant. There are better ways to do this
# for example, use a dictionary to store the field names and types. This would allow for reuse in the "insert" segment
myCursor.execute('CREATE TABLE midsummer(line_number INTEGER PRIMARY KEY, cast_name TEXT, play_text TEXT);')
myCursor.execute('CREATE TABLE performanceStats(action TEXT,duration REAL);')

#####
# get the list of characters and place into a list

start_stopwatch = time.time()

with open('characters.txt') as play_characters:
    listOfCharacters = play_characters.read().splitlines()

#####
# build the play text table

currentCharacter = "NoNameCharacter"

# Note: SQLite3 execute() prefers "?" over "%s"
sqlToDo = "INSERT INTO midsummer (cast_name,play_text) VALUES (?,?)"


with open("A_Midsummer_Nights_Dream.txt") as aLineInPlay:
    for line in aLineInPlay:
        if line.upper().strip() in listOfCharacters:
            currentCharacter = line.upper().strip()
        else:
            argsToPass = currentCharacter,line
            myCursor.execute(sqlToDo,argsToPass)

conn.commit()

####
# Figure how long this took

end_stopwatch = time.time()

myCursor.execute('SELECT max(line_number) FROM midsummer')

linesInPlay = myCursor.fetchall()[0][0]

stopwatch = end_stopwatch - start_stopwatch

lines_duration = stopwatch/linesInPlay

SQLToDo = 'INSERT INTO performanceStats(action,duration) VALUES ("CREATE",?)'

myCursor.execute(SQLToDo,(lines_duration,))

conn.commit()
