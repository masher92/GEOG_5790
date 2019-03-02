"""
File which:
Open a connection to a database and trials means of extracting information from it.

@author Molly Asher
@Version 1.0
"""

import os
import sqlite3

# Set working directory
os.chdir("E:/Msc/Advanced-Programming/Github/GEOG_5790/Practical5-SQLite")

# Connect to pre-existing database
conn = sqlite3.connect('resultsdb.sqlite')

# Get a cursor from the connection to interact with the database.
c = conn.cursor()

# Read the table rows, and print (various options)
for row in c.execute('SELECT * FROM Results ORDER BY burglaries'):
    # Print the first value in each row:
    print(row[0])
    # Print everything in the row.
    print(row) 
    # Print everything in the row formatted (with option to change order)
    print(u'{0}, {1}'.format(row[0], row[1]))
    # Print with added text.
    print(u'{1} burglaries have happened at the {0}'.format(row[0], row[1]))

    
# Find column names 
c = conn.execute('SELECT * FROM Results')
for description in c.description:
	print(description[0]) # Name - note that [1]…[6] are Nones.



#######
# execute an SQL command,
c.execute("SELECT * FROM Results") 
# Executing the command doesn't return the results, need to run another command 
# to fetch the results. 
print("fetchall:")
result = c.fetchall() 
for r in result:
    print(r)
c.execute("SELECT * FROM Results") 
print("\nfetch one:")
res = c.fetchone() 
print(res)


c.execute("COUNT burglaries AS colForAnswers")
c.execute("SELECT address, COUNT(DISTINCT address) AS HousesAffected FROM Results")
result = c.fetchall() 
for r in result:
    print(r)
