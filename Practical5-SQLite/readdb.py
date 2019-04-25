"""
File which:
Open a connection to a database and trials means of extracting information from it.

@author Molly Asher
@Version 1.0
"""

import os
import sqlite3

# Set working directory
os.chdir("E:/Msc/Advanced-Programming/GitHub/GEOG_5790/Practical5-SQLite")
print("Working directory at: ", os.getcwd())

# Connect to pre-existing database
conn = sqlite3.connect('resultsdb.sqlite')
print ("Connected to Results Database")

# Find column names 
c = conn.execute('SELECT * FROM Results')
print ("Column names are: ")
for description in c.description:
	print(description[0])

# Get a cursor from the connection to interact with the database.
c = conn.cursor()

# Read the table rows, and print (various options)
print ("The values are:")
for row in c.execute('SELECT * FROM Results ORDER BY burglaries'):
    print ("For the row: ", row)
    # Print the first value in each row:
    print("First value: ", row[0])
    # Print everything in the row formatted (with option to change order)
    print("Everything: " , u'{0}, {1}'.format(row[0], row[1]))
    # Print with added text.
    print(u'Meaning that: {1} burglaries have happened at the {0}'.format(row[0], row[1]))
   
# An alternative method to view the results:
c.execute("SELECT * FROM Results") 
# Executing the command doesn't return the results, need to run another command 
# to fetch the results. 
print("All the results:")
result = c.fetchall() 
for r in result:
    print(r)
c.execute("SELECT * FROM Results") 
print("One of the results")
res = c.fetchone() 
print(res)



