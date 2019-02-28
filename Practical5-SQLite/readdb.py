# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 21:37:50 2019

@author: Molly
"""

import os
import sqlite3

# 1. Write connection code, make database table, fill it with information.
os.getcwd()
os.chdir("E:/Msc/Advanced-Programming/Practical5-SQLite")

# Connect to database - resultsdb
conn = sqlite3.connect('resultsdb.sqlite')

# Get a cursor from the connection to interact with the database.
c = conn.cursor()

# Execute the following Python to read the table rows and print the first value in each row:
for row in c.execute('SELECT * FROM Results ORDER BY burglaries'):
    # Print using old style string formatting, see https://realpython.com/python-string-formatting/
    print(u'{0}, {1}'.format(row[0], row[1]))
    print(u'{1}, {0}'.format(row[0], row[1]))
    print(u'{0}, {1}'.format(row[1], row[0]))
    #print('{1} burglaries have happened at {0}')
    print(row[0])     
    print(row)  
    
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
