#!/usr/bin/env python3
"""
MFND - A simple to-do list application
"""

import datetime
import sqlite3
import os

def main():

    # Initialize the database
    initDatabase()

    # While not done print status and get input
    done = False
    while (not done):
        printStatus()
        done = getResponse()


def initDatabase():
    x = 0
    #scriptPath = os.path.dirname(os.path.realpath(__file__))
    #databasePath = scriptPath + "/../data/todo_list.sqlite"

    #conn = sqlite3.connect(databasePath)
    #c = conn.cursor()

    # # Create table
    #c.execute('''CREATE TABLE stocks
    #          (date text, trans text, symbol text, qty real, price real)''')
        # # Insert a row of data
    # c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # # Save (commit) the changes
    # conn.commit()

    # # We can also close the connection if we are done with it.
    # # Just be sure any changes have been committed or they will be lost.
    # conn.close()

def printStatus():
    today = datetime.date.today()

    print("")
    print( today.strftime("MFND - %B %d, %Y") )
    print("")
    print("  1. Put cover sheet on TPS report")
    print("  2. Run 5 miles")
    print("  3. Floss")
    print("")

def getResponse():
    response = raw_input("> ")
    if (response == "exit"):
        print("MFND exiting...")
        return True

    return False

if  __name__ =='__main__':
    main()
