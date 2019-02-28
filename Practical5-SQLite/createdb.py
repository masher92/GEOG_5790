# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 19:55:30 2019

@author: Molly
"""

import os
import sqlite3

# 1. Write connection code, make database table, fill it with information.
os.getcwd()
os.chdir("E:/Msc/Advanced-Programming/Practical5-SQLite")

# Connect to database - resultsdb
# Create a connection object that represents the database, c
conn = sqlite3.connect('resultsdb.sqlite')

# Get a cursor from the connection to interact with the database.
c = conn.cursor()

# Create a table - the data saved is persistent and available in subsequent sessions.
# (Call cursor's execute method to perform SQl commands)
c.execute("CREATE TABLE Results (address text, burglaries integer)")
# Insert data into the table
c.execute("INSERT INTO Results VALUES ('Queen Vic',2), ('Laundrette', 3)")
# Commit the changes
conn.commit()
# Close the connection
conn.close()


