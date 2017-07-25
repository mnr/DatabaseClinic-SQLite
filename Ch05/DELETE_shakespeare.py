#!/bin/env python2.7

"""
For each record in the database,
DELETE any lines that
start with "ENTER"
or "EXIT"
or "ACT"
or "SCENE"
"""

import sqlite3 # provides python with a library for sqlite
import time

conn = sqlite3.connect("shakespeare.sqlite") # opens sqlite and a database file
myCursor = conn.cursor() # provides a connection to the database

myCursor.execute('SELECT max(line_number) FROM midsummer')

linesInPlay = myCursor.fetchall()[0][0]

start_stopwatch = time.time() #start a timer

sqlToDo = "DELETE FROM midsummer "
sqlToDo += "   WHERE ( "
sqlToDo += '      play_text LIKE "ENTER%" '
sqlToDo += '   OR play_text  LIKE "EXIT%" '
sqlToDo += '   OR play_text  LIKE "ACT%" '
sqlToDo += '   OR play_text  LIKE "EXEUNT%" '
sqlToDo += '   OR play_text  LIKE "SCENE%" '
sqlToDo += '   )'
sqlToDo += ';'

myCursor.execute(sqlToDo)

conn.commit()

####
# Figure how long this took

end_stopwatch = time.time()

stopwatch = end_stopwatch - start_stopwatch

lines_duration = stopwatch/linesInPlay

SQLToDo = 'INSERT INTO performanceStats(action,duration) VALUES ("DELETE",?)'

myCursor.execute(SQLToDo,(lines_duration,))

conn.commit()
