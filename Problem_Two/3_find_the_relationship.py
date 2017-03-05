#!/bin/env python2.7

# this code assumes 1_import_calEnviro.py and 2_add_population_projections.py have already run
# Asthma = Age-adjusted rate of emergency department visits for asthma

import sqlite3 # provides python with a library for sqlite

# opens sqlite and a database file
conn = sqlite3.connect("calEnviro.sqlite") 

myCursor = conn.cursor() # provides a connection to the database

myCursor.execute('DROP TABLE IF EXISTS ethVsAsthma;')

doThisSQL = ( 'CREATE TABLE ethVsAsthma as '
              'select '
              '"County Name" , '
              '"Race Name", '
              'SUM(Population), '
              'avgAsthma '
              'FROM '
              '   ('
              '    SELECT AVG(Asthma) AS avgAsthma, "California County" '
              '    FROM CalEnviro '
              '    GROUP BY "California County" '
              '   ) '
              'INNER JOIN CA_PopulationProj  '
              'ON "California County" = "County Name" '
              'WHERE Year = "01/01/2010 12:00:00 AM" '
              'GROUP BY "County Name", "Race Name" '
              'ORDER BY "Race Name" '
              ';')


myCursor.execute(doThisSQL)

# table ethVsAsthma now contains something like this...

# County...Race Name...Population...Average Asthma instances
# (u'Imperial', u'Multi-Race', 1033, 75.92552190322579)
# (u'Imperial', u'Pacific Islander', 104, 75.92552190322579)
# (u'Imperial', u'White', 24450, 75.92552190322579)
# (u'Tehama', u'American Indian', 1239, 78.4671299090909)
# (u'Tehama', u'Asian', 653, 78.4671299090909)


# SQLite doesn't have standard deviation, so I take the sql result and run it through scipy for correlation

# my plan is to...
# 1) For each Ethnicity...
# !) Create Two lists per Ethnicity
#     A) Ethnicity: population by county
#     B) Ethnicity: Average asthma incidents by county
# 2) Run pearsonr (from scipy) on those lists
# 3) print Ethnicity vs r vs P-Value

# I need a list of all ethnicities. SQLite to the rescue

SQL_for_all_Ethnicities = ('select Distinct """Race Name""" from ethVsAsthma;')

myCursor.execute(SQL_for_all_Ethnicities)

listOfEthnicities = myCursor.fetchall()

from scipy.stats.stats import pearsonr      

for anEthnicity in listOfEthnicities:
    anEthnicity = anEthnicity[0]
    SQL_for_popVcnty = ('select "SUM(Population)" FROM ethVsAsthma WHERE """Race Name""" = "' + anEthnicity + '" ;')
    myCursor.execute(SQL_for_popVcnty)
    populationVcounty = myCursor.fetchall();

    SQL_for_asthmaVcnty = ('select avgAsthma FROM ethVsAsthma WHERE """Race Name""" = "'+ anEthnicity +'" ;')
    myCursor.execute(SQL_for_asthmaVcnty)
    asthmaVcounty = myCursor.fetchall();
    pearson_r,pearson_p = pearsonr(populationVcounty,asthmaVcounty)
    pearson_r = pearson_r[0]
    pearson_p = pearson_p[0]

    if pearson_r == -1:
        print "There is a perfect negative relationship",
    elif pearson_r < -.7:
        print "There is a strong negative relationship",
    elif pearson_r < -.5:
        print "There is a moderately negative relationship",
    elif pearson_r < -.3:
        print "There is a weak negative relationship",
    elif pearson_r <= 0:
        print "There is no relationship",
    elif pearson_r < .3:
        print "There is a weak positive relationship",
    elif pearson_r < .5:
        print "There is a moderately positive relationship",
    elif pearson_r < .7:
        print "There is a strong positive relationship",
    elif pearson_r == 1:
        print "There is a perfect positive relationship",
    else:
        print "pearson_r value doesn't make sense. It is " + pearson_r

    print "between Asthma and " + anEthnicity + " ethnicity."
    


