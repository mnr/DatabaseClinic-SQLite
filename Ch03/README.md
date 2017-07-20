# Join Two Datasets

In this chapter of Database Clinic, we're asked to start with two datasets, then, extract, transform and load them into the database of their choice.

We’ll be working with road safety data published by the [UK government at their open data website.](https://data.gov.uk/dataset/road-accidents-safety-data)

To get this data, download two files:
[2015 Road Safety - all 2015 data](http://data.dft.gov.uk/road-accidents-safety-data/RoadSafetyData_2015.zip)
... and ...
[Lookup up tables for variables (which unpacks into road-accidents-safety-data)](http://data.dft.gov.uk/road-accidents-safety-data/Road-Accident-Safety-Data-Guide.xls)

Unzip these files, then place them into the folder that contains this code.

This data contains several fields:
### Accidents_2015.csv
1. Accident_Severity
2. Accident_Index

### Vehicles_2015.csv
1. Vehicle_Type
2. Accident_Index

There is a third file, which contains definitions of the various data types. Most importantly, it provides descriptive vehicle types.:
### Road-Accident-Safety-Data-Guide.xls
* Table titled Vehicle Type

We’re asked to determine the median accident severity for each type of motorcycle. This will show if there is any relationship between the type of motorcycle and the types of accidents they are involved in.

We know that Accident_Index is a common link between the databases and we can use that link to create a relationship between the datasets.

## MNR Notes

To solve this problem, I wrote four python scripts:
1. Import Accidents_2015.csv into a SQLite Database
2. Import Vehicles_2015.csv into the SQLite Database.
3. Import the lookup table from the excel files
4. Calculate the average

These scripts demonstrate how to use SQLite with a programming language and they also keep the four steps in neat packages.

### 1_import_accidents.py
This python program imports the accident data. It's written without error trapping with the intent of focus on the solution. Your version should include error trapping so it is more resilient.

My code uses sqlite3, a python library with support for sqlite.

This is a somewhat graceless solution. I've done this to clearly illustrate certain points. There are better ways to do this and I'll show them in the next python program.

### 2_import_vehicles.py
This python script imports the vehicle data in Vehicles_2015.csv. It is a bit more graceful when importing the data because it doesn't require naming every column.

### 3_import_excel_tables.py
Loads in two tabs from the excel file: accident_severity and vehicle_type. This requires installing xlrd. I've often experienced "ImportError: No module named xlrd" even after doing "sudo pip install xlrd". I've resorted to adding the xlrd.egg to PYTHONPATH by doing the following in a terminal: "export PYTHONPATH=$PYTHONPATH: where-ever-pip-installed-the-xlrd.egg"

### 4_calculate_median.py
SQLite doesn't have a function to produce median, so I've used python's conn.create_function to add it. For extra credit, it also calculates the average severity.

## I've also produced a solution written in R
### dbjoins.R
A solution written using the R programming language. Includes all steps as outlined above. RSQLite uses "RSQLite::initExtension(db)" to add a package of statistic functions.
