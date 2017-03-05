Database Mayhem!
CRUD concepts
We will provide the text of a Shakespeare play ( http://shakespeare.mit.edu/midsummer/full.html converted to a text file) as well as a second text file containing the names of characters in the play. Using that text, the DB Clinic author will write four programs to accomplish the following concurrent tasks:
For each line in the Shakespeare text, CREATE a corresponding record in the database. Each record will include the name of the character speaking, the (absolute) line number of the phrase and the phrase itself, trimmed of any leading or following spaces 
For each record in the database, search for character names, convert them to UPPERCASE, then UPDATE the record in the database
For each record in the database, DELETE any lines that start with “ENTER” or “EXIT” or “ACT” or “SCENE”
When all other tasks are complete, READ each line and print it out to console. This task is not concurrent.
During execution, store performance data and then create the following table:
