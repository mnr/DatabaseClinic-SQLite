# Problem 2 : Database Joins

Given a data set of road accidents, calculate the average accident severity for every type of motorcycle.

This problem demonstrates simple relational concepts.

Start with the [UK Road data found here.](https://data.gov.uk/dataset/road-accidents-safety-data) This includes several data files and some look up tables.

Given these fields from these two datasets:

## Accidents_2015.csv
1. Accident_Severity
2. Accident_Index

## Vehicles_2015.csv
1. Vehicle_Type
2. Accident_Index

...and this value lookup table:
## Road-Accident-Safety-Data-Guide.xls
* Table titled Vehicle Type

**...Calculate the average accident severity for every type of motorcycle**

To solve this problem, I wrote four python scripts:
1. Import Accidents_2015.csv into a SQLite Database
2. Import Vehicles_2015.csv into the SQLite Database.
3. Import the lookup table from the excel files
4. Calculate the average

These scripts demonstrate how to use SQLite with a programming language and they also keep the four steps in neat packages.

# My Solution
## 1_import_accidents.py
This python program imports the accident data. It's written without error trapping with the intent of focus on the solution. Your version should include error trapping so it is more resilient. 

My code uses sqlite3, a python library with support for sqlite. 

This is a somewhat graceless solution. I've done this to clearly illustrate certain points. There are better ways to do this and I'll show them in the next python program.

## 2_import_vehicles.py
## 3_import_excel_tables.py
## 4_calculate_average.py
## dbjoins.R
A solution written using the R programming language. Includes all steps as outlined above.
