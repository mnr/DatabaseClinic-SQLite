#!/bin/env python2.7

"""
When all other tasks are complete,
READ each line and print it out to console.
"""

import sqlite3 # provides python with a library for sqlite
import time

conn = sqlite3.connect("shakespeare.sqlite") # opens sqlite and a database file
myCursor = conn.cursor() # provides a connection to the database

myCursor.execute('SELECT max(line_number) FROM midsummer')

linesInPlay = myCursor.fetchall()[0][0]

start_stopwatch = time.time() #start a timer

myCursor.execute('SELECT play_text from midsummer')

for aline in myCursor.fetchall():
    print aline[0]
####
# Figure how long this took

end_stopwatch = time.time()

stopwatch = end_stopwatch - start_stopwatch

lines_duration = stopwatch/linesInPlay

SQLToDo = 'INSERT INTO performanceStats(action,duration) VALUES ("READ",?)'

myCursor.execute(SQLToDo,(lines_duration,))


conn.commit()
