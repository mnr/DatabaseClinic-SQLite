# Problem 4 : CRUD concepts

This challenge will demonstrate how to perform [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) operations on a range of databases.

There are several tasks to perform. We are provided with the text of Shakespeare’s [A Midsummer Night's Dream](http://shakespeare.mit.edu/midsummer/full.html), plus a list of characters in the play. Using those two datasets, the instructors will have to accomplish the following tasks. The first 3 tasks will execute concurrently (if possible/practical).

* For each line in the Shakespeare text, **CREATE** a corresponding record in the database. Each record will include the name of the character speaking, the (absolute) line number of the phrase and the phrase itself, trimmed of any leading or following spaces
* For each record in the database, search for character names, convert them to UPPERCASE, then **UPDATE** the record in the database
* For each record in the database, **DELETE** any lines that start with “ENTER” or “EXIT” or “ACT” or “SCENE”
* When all other tasks are complete, **READ** each line and print it out to console. This task is not concurrent.
* During execution, the instructor will store performance data and then create a table showing the average time for each operation:


| Operation | Average Execution Time (Milliseconds) |
|---|---|
| CREATE | (average time for each line of task 1) |
| READ | (average time for each line of task 4) |
| UPDATE | (average time for each line of task 2) |
| DELETE | (average time for each line of task 3) |

# Exercise Files
For this chapter, the files will be provided in the Exercise Files:
A_Midsummer_Nights_Dream.txt for the play’s text
characters.txt for the character list.

# MNR Notes
This problem wasn't all that difficult. I've broken my solution into four python programs that store performance data back into the database for use by the timing report.

I've also provided an "R" version of the solution.
