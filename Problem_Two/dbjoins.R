#!/usr/bin/Rscript

# Copyright Mark Niemann-Ross, 2017
# Author: Mark Niemann-Ross. mark.niemannross@gmail.com
# Description: lynda.com, Database Clinic, SQLite, Problem 2

# import necessary libraries
list.of.packages <- c("RSQLite","readxl")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

#SQLite support
library(RSQLite)

putSQLiteHere <- "myRsqlite.sqlite"
mySQLiteDB <- dbConnect(RSQLite::SQLite(),putSQLiteHere)

# this is a function to import zip files, unpack them, then load them into an sqlite db
importDataset <- function(getThisDataSet) {
  completePathName <- paste0("http://data.dft.gov.uk/road-accidents-safety-data/",getThisDataSet,".zip")
  mytempfile <- tempfile()
  download.file(completePathName,mytempfile)
  mydatafromcsv <- read.csv(unzip(mytempfile))
  dbWriteTable(conn=mySQLiteDB,name = getThisDataSet,value=mydatafromcsv)
  file.remove(mytempfile)
}

filestoget <- c("RoadSafetyData_Accidents_2015","RoadSafetyData_Vehicles_2015")
sapply(filestoget,importDataset)

# import the sheets from the excel file
library(readxl)
url <- "http://data.dft.gov.uk/road-accidents-safety-data/Road-Accident-Safety-Data-Guide.xls"
destfile <- "Road_Accident_Safety_Data_Guide.xls"
download.file(url, destfile)

putTheseSheetsInSQLite <- function(sheetWeNeed) {
  aSheetFromExcel <- read_excel(destfile,sheet=sheetWeNeed)
  dbWriteTable(conn=mySQLiteDB,name = sheetWeNeed,value=aSheetFromExcel)
  }

importTheseSheets <- c("Accident Severity","Vehicle Type")
sapply(importTheseSheets,putTheseSheetsInSQLite)

# Calculate the average accident severity for every type of motorcycle
#
do_this_sqlite <- "
SELECT avg(Accident_Severity) as Severity,label
FROM RoadSafetyData_Accidents_2015
LEFT JOIN RoadSafetyData_Vehicles_2015 ON RoadSafetyData_Accidents_2015.Accident_Index = RoadSafetyData_Vehicles_2015.Accident_Index
LEFT JOIN `Vehicle Type` ON cast(Vehicle_Type as REAL) LIKE `Vehicle Type`.code
WHERE Label LIKE '%otorcycle%'
GROUP BY label
ORDER BY Severity"
dbGetQuery(mySQLiteDB,do_this_sqlite)
