#!/usr/bin/Rscript

# Copyright Mark Niemann-Ross, 2017
# Author: Mark Niemann-Ross. mark.niemannross@gmail.com
# Description: lynda.com, Database Clinic, Shakespeare, Problem 4

# SETUP -------------------------------------------------------------------

# import necessary libraries
list.of.packages <- c("tictoc")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)


# tictoc provides matlab-like timers
library(tictoc)
tic.clearlog()

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
tic("Create")

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
    
    sqlToDo <- "INSERT INTO midsummer (cast_name,play_text) VALUES (:x, :y)"
    sqlParms <- list(x=character.speaking,y=oneLine)
    
    dbResult <- dbSendStatement(mySQLiteDB, sqlToDo,params = sqlParms)
    dbClearResult(dbResult)
    
  }
}

toc(log=TRUE) # Stop the clock

close(shakes.connection) # close the Shakespeare text file

sqlToDo <- "SELECT max(line_number) FROM midsummer"
lines.in.midsummer <- dbGetQuery(mySQLiteDB,sqlToDo)[1,1]

# UPDATE ------------------------------------------------------------------


### For each record in the database, search for character names, convert them to
#   UPPERCASE, then UPDATE the record in the database

tic("Update")

for (acharacter in list.of.characters) {
  # titled produces a first letter cap. R doesn't have toTitle()
  titled.acharacter <- paste0(substring(acharacter,1,1),tolower(substring(acharacter,2)))
  
  sqlToDo <- "UPDATE midsummer SET play_text = REPLACE(play_text,:x,:y) WHERE instr(play_text,:z)"
  sqlParms <- list(x=titled.acharacter,y=toupper(acharacter),z=titled.acharacter)
  
  dbResult <- dbSendStatement(mySQLiteDB, sqlToDo,params = sqlParms)
  dbClearResult(dbResult)
}

toc(log=TRUE) # Stop the clock

# DELETE ------------------------------------------------------------------


### For each record in the database, DELETE any lines that start with “ENTER” or
#   “EXIT” or “ACT” or “SCENE”

tic("Delete")

sqlToDo <- 'DELETE FROM midsummer WHERE (play_text LIKE "ENTER%" OR play_text LIKE "EXIT%" OR play_text  LIKE "ACT%" OR play_text  LIKE "SCENE%" );'
dbResult <- dbSendStatement(mySQLiteDB, sqlToDo)
dbClearResult(dbResult)

toc(log=TRUE) # Stop the clock



# READ --------------------------------------------------------------------


### When all other tasks are complete, READ each line and print it out to
#   console. This task is not concurrent.

options(max.print = lines.in.midsummer + 10)

tic("Read")

dbGetQuery(mySQLiteDB,"SELECT play_text from midsummer")

toc(log=TRUE) # Stop the clock


# PERFORMANCE STATISTICS --------------------------------------------------


# During execution, store performance data and then create the following table:

for(aTic in tic.log(format=FALSE)) {
  mseconds <- (aTic[[2]]-aTic[[1]])/lines.in.midsummer
  #mseconds <- 0
  print(paste(aTic[3],mseconds))
}

dbDisconnect(mySQLiteDB) # close the database

