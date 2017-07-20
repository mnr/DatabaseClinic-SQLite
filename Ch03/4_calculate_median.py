#!/bin/env python2.7

# Calculate the median accident severity for every type of motorcycle

import sqlite3 # provides python with a library for sqlite

SQLITE_FILE = "UKRoadData.sqlite"
conn = sqlite3.connect(SQLITE_FILE)
myCursor = conn.cursor()


# SQLite does not have a "median" function. Use create_function
# first, create a function to calculate median
def calcMedian(theListofValues):
    quotient, remainder = divmod(len(theListofValues),2)
    if remainder:
        return sorted(theListofValues)[quotient]
    return sum(sorted(theListofValues)[quotient - 1:quotient + 1]) / 2

# then install the function in sqlite
conn.create_function("median",1,calcMedian)


do_this_sqlite = """
SELECT median(Accident_Severity),avg(Accident_Severity) as Severity,Label
FROM Accidents_2015
LEFT JOIN Vehicles_2015 ON Accidents_2015.Accident_Index = Vehicles_2015.Accident_Index
LEFT JOIN vehicle_type ON Vehicle_Type LIKE vehicle_type.Code
WHERE Label LIKE "%otorcycle%"
GROUP BY Label
ORDER BY Severity
"""

print '{:<12} {}'.format("Med Severity","Avg Severity","Motorcycle")
for aRow in myCursor.execute(do_this_sqlite):
    print '{:.11} {:.3} {}'.format(aRow[0],aRow[1],aRow[2])
