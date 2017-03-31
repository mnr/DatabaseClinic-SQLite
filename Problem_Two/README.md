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
