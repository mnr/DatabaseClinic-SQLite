#!/bin/env python2.7

# Calculate the average accident severity for every type of motorcycle

import sqlite3 # provides python with a library for sqlite

SQLITE_FILE = "UKRoadData.sqlite"
conn = sqlite3.connect(SQLITE_FILE)
myCursor = conn.cursor()


do_this_sqlite = """
SELECT avg(Accident_Severity) as Severity,Label
FROM Accidents_2015
LEFT JOIN Vehicles_2015 ON Accidents_2015.Accident_Index = Vehicles_2015.Accident_Index
LEFT JOIN vehicle_type ON Vehicle_Type LIKE vehicle_type.Code
WHERE Label LIKE "%otorcycle%"
GROUP BY Label
ORDER BY Severity
"""

print '{:<12} {}'.format("Avg Severity","Motorcycle")
for aRow in myCursor.execute(do_this_sqlite):
    print '{:.11} {}'.format(aRow[0],aRow[1])

