#!/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Access the 200 most recent APODs by date. Start with today, then move back 200 days, one day at a time.
Create fields in your database for copyright, date, Explanation, Title. Store appropriate metadata information in each
Store the hdurl image in the database as a blob (or whatever datatype is appropriate)
Start a timer
Search database.explanation for the word “Solar” (the number of hits doesn’t matter - we’re only interested in the time it takes.)
Stop the timer
Calculate the size of the database
In a separate table, record the size of the database compared to the time to complete the search

"""

import sqlite3
import json
import urllib2
from datetime import datetime, timedelta
import time

conn = sqlite3.connect("apod.sqlite") # opens sqlite and a database file
myCursor = conn.cursor() # provides a connection to the database
myCursor.execute('CREATE TABLE apod(apodDate TEXT, explanation TEXT, title TEXT,hdImage BLOB);')
myCursor.execute('CREATE TABLE performanceStats(dbsize INTEGER,duration REAL);')


writeMetaData_SQL = 'INSERT INTO apod (apodDate,explanation,title) VALUES (?,?,?);'
writeImage_SQL = 'UPDATE apod SET hdImage=? WHERE rowID=last_insert_rowid();'
searchForSolar_SQL = 'SELECT COUNT(title) FROM apod WHERE explanation LIKE "%Solar%";'
writePerformance_SQL = 'INSERT INTO performanceStats(dbsize,duration) VALUES (?,?);'

authKey = 'get an authkey from https://api.nasa.gov/index.html#apply-for-an-api-key'

lastRowInserted = 0
dateCounter = 0

while lastRowInserted < 200:
    # get 200 images by date, starting with today and going backwards
    datePointer = datetime.today() - timedelta(days=dateCounter)
    useThisDate = datePointer.strftime('%Y-%m-%d')
    theURL = 'https://api.nasa.gov/planetary/apod?api_key={0}&date={1}'.format(authKey,useThisDate)
    try:
        apodResponse = urllib2.urlopen(theURL)
    except urllib2.URLError as e:
        print e.reason
    except urllib2.HTTPError as e:
        print e.reason
    else:
        apodDataRaw = apodResponse.read()
        apodData = json.loads(apodDataRaw)

        # get the rate limit from NASA
        for listitem in apodResponse.info().headers:
            if "X-RateLimit-Remaining" in listitem:
                apodRateLimit = listitem
        # provide an indicator of where we are
        print(apodData['date'],apodRateLimit,apodData['title'])


    if 'hdurl' in apodData:
        # save the meta data
        executeValues = (apodData['date'],apodData['explanation'],apodData['title'])
        myCursor.execute(writeMetaData_SQL,executeValues)

        # get and save the hi res image
        apodHDImgResponse = urllib2.urlopen(apodData['hdurl'])
        apodHDImage = apodHDImgResponse.read()
        myCursor.execute(writeImage_SQL,[sqlite3.Binary(apodHDImage)])
        conn.commit()

        # time the search for "Solar"
        start_stopwatch = time.time()
        myCursor.execute(searchForSolar_SQL)
        end_stopwatch = time.time()
        stopwatch = end_stopwatch - start_stopwatch

        # get db size
        howManyPagesRaw = myCursor.execute('PRAGMA page_count')
        howManyPages = howManyPagesRaw.fetchone()[0]
        howBigPagesRaw = myCursor.execute('PRAGMA page_size')
        howBigPages = howBigPagesRaw.fetchone()[0]
        theDBSize = howManyPages * howBigPages

        # save performance data
        myCursor.execute(writePerformance_SQL,(theDBSize,stopwatch))
        conn.commit()

    # set up for next while loop
    dateCounter += 1
    lastRowRaw = myCursor.execute('SELECT last_insert_rowid();')
    lastRowInserted = lastRowRaw.fetchone()[0]
