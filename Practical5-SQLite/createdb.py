"""
File which:
Creates a connection to a database, produces a table and fills it with info.
@author Molly Asher
@Version 1.0
"""

import os
import sqlite3

# Set working directory
os.chdir("E:/Msc/Advanced-Programming/GitHub/GEOG_5790/Practical5-SQLite")

# Create a database - resultsdb -  and create a connection to it. 
conn = sqlite3.connect('resultsdb.sqlite')

# Get a cursor from the connection to interact with the database.
c = conn.cursor()

# Create a table (by calling cursor's execute method to perform SQL)
c.execute("CREATE TABLE Results (address text, burglaries integer)")
# Insert data into the table
c.execute("INSERT INTO Results VALUES ('Queen Vic',2), ('Laundrette', 3)")
# Commit the changes
conn.commit()
# Close the connection
conn.close()


