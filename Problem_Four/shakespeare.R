#!/usr/bin/Rscript

# Copyright Mark Niemann-Ross, 2017
# Author: Mark Niemann-Ross. mark.niemannross@gmail.com
# Description: lynda.com, Database Clinic, Shakespeare, Problem 4

# uses the RSQLite package for SQLite support
library(DBI)

putSQLiteHere <- "shakespeare.sqlite" # could also be ":memory:"
mySQLiteDB <- dbConnect(RSQLite::SQLite(), dbname = putSQLiteHere)

list.of.characters <- readLines("characters.txt")
character.speaking <- "NoNameCharacter"
timer.results <-
  c() # will contain times for create, read, update, delete

dbResult <- dbSendStatement(
  mySQLiteDB,
  'CREATE TABLE midsummer(line_number INTEGER PRIMARY KEY, cast_name TEXT, play_text TEXT);'
)
dbClearResult(dbResult)


# For each line in the Shakespeare text,
Shakes.text <- "A_Midsummer_Nights_Dream.txt"
shakes.connection <- file(Shakes.text, open = "r")

# CREATE ------------------------------------------------------------------

### For each line in the Shakespeare text, CREATE a corresponding record in the
#   database. Each record will include the name of the character speaking, the
#   (absolute) line number of the phrase and the phrase itself, trimmed of any
#   leading or following spaces


# Start the clock for CREATE
ptm <- proc.time()['sys.self']

while (length(oneLine <-
              readLines(shakes.connection, n = 1, warn = FALSE)) > 0) {
  oneLine <- trimws(oneLine)
  # CREATE a corresponding record in the database.
  # Each record will include the name of the character speaking,
  if (oneLine %in% list.of.characters) {
    character.speaking <- oneLine
  } else {
    # add the phrase itself,
    # trimmed of any leading or following spaces
    
    sqlToDo = paste0(
      'INSERT INTO midsummer (cast_name,play_text) VALUES (',
      '"', character.speaking,'"',
      ',',
      '"', oneLine,'"',
      ')'
    )
    dbResult <- dbSendStatement(mySQLiteDB, sqlToDo)
    dbClearResult(dbResult)
    
  }
}
# Stop the clock
timer.results["Create"] <- proc.time()['sys.self'] - ptm

close(shakes.connection) # close the Shakespeare text file

sqlToDo <- "SELECT max(line_number) FROM midsummer"
lines.in.midsummer <- dbGetQuery(mySQLiteDB,sqlToDo)[1,1]

# UPDATE ------------------------------------------------------------------


### For each record in the database, search for character names, convert them to
#   UPPERCASE, then UPDATE the record in the database

# Start the clock for UPDATE
ptm <- proc.time()['sys.self']

for (acharacter in list.of.characters) {
  # titled produces a first letter cap. R doesn't have toTitle()
  titled.acharacter <- paste0(substring(acharacter,1,1),tolower(substring(acharacter,2)))
  sqlToDo <- paste0(
    "UPDATE midsummer ",
    "SET play_text = ",
    "REPLACE(play_text, ",
         '"',titled.acharacter,'",',
         '"',toupper(acharacter),'"',
         ") ",
    "WHERE instr(play_text,",'"',titled.acharacter,'"',")"
  )
  dbResult <- dbSendStatement(mySQLiteDB, sqlToDo)
  dbClearResult(dbResult)
}
# Stop the clock
timer.results["Update"] <- proc.time()['sys.self'] - ptm


# DELETE ------------------------------------------------------------------


### For each record in the database, DELETE any lines that start with “ENTER” or
#   “EXIT” or “ACT” or “SCENE”

# Start the clock for DELETE
ptm <- proc.time()['sys.self']

sqlToDo <- 'DELETE FROM midsummer WHERE (play_text LIKE "ENTER%" OR play_text LIKE "EXIT%" OR play_text  LIKE "ACT%" OR play_text  LIKE "SCENE%" );'
dbResult <- dbSendStatement(mySQLiteDB, sqlToDo)
dbClearResult(dbResult)

# Stop the clock
timer.results["Delete"] <- proc.time()['sys.self'] - ptm


# READ --------------------------------------------------------------------


### When all other tasks are complete, READ each line and print it out to
#   console. This task is not concurrent.

# PERFORMANCE STATISTICS --------------------------------------------------


# During execution, store performance data and then create the following table:

dbDisconnect(mySQLiteDB) # close the database

