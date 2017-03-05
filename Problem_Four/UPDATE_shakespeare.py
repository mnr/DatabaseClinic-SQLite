#!/bin/env python2.7

"""
For each record in the database,
search for character names,
convert them to UPPERCASE,
then UPDATE the record in the database
"""

import sqlite3 # provides python with a library for sqlite
import time

conn = sqlite3.connect("shakespeare.sqlite") # opens sqlite and a database file
myCursor = conn.cursor() # provides a connection to the database

myCursor.execute('SELECT max(line_number) FROM midsummer')

linesInPlay = myCursor.fetchall()[0][0]
linesProcessed = 0

start_stopwatch = time.time() #start a timer

with open('characters.txt') as play_characters:
    for acharacter in play_characters.read().splitlines():
        sqlToDo = "UPDATE midsummer SET play_text = REPLACE(play_text, "
        sqlToDo += '"' + acharacter.capitalize() + '", '
        sqlToDo += '"' + acharacter.upper() + '") '
        sqlToDo += "WHERE instr(play_text,"
        sqlToDo += '"' + acharacter.capitalize() + '")'
        myCursor.execute(sqlToDo)
        # print acharacter
        linesProcessed += linesInPlay

conn.commit()

####
# Figure how long this took

end_stopwatch = time.time()

stopwatch = end_stopwatch - start_stopwatch

lines_duration = stopwatch/linesProcessed

SQLToDo = 'INSERT INTO performanceStats(action,duration) VALUES ("UPDATE",{0})'.format(lines_duration)

myCursor.execute(SQLToDo)

conn.commit()
