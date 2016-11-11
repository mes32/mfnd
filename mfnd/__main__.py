#!/usr/bin/env python3
"""
MFND - A simple to-do list application
"""

import datetime
import sqlite3
import os

def main():

    # Initialize the database
    databasePath = initDatabase()

    # While not done print status and get input
    done = False
    while (not done):
        printStatus(databasePath)
        done = getResponse()


def initDatabase():
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    databasePath = scriptPath + "/../data/todo_list.sqlite"

    conn = sqlite3.connect(databasePath)
    c = conn.cursor()

    # Create table
    sql = '''CREATE TABLE IF NOT EXISTS TodoTask (
                 description TEXT NOT NULL, 
                 completionStatus INT NOT NULL, 
                 visible INT, 
                 mode_id INT
             );'''
    c.execute(sql)

    # Insert some sample rows
    sql = '''INSERT INTO TodoTask (
                 description,
                 completionStatus
             ) VALUES (
                 'Put cover sheet on TPS report',
                 0
             );'''
    c.execute(sql)
    sql = '''INSERT INTO TodoTask (
                 description,
                 completionStatus
             ) VALUES (
                 'Put cover sheet on TPS report',
                 0
             );'''
    c.execute(sql)
    sql = '''INSERT INTO TodoTask (
                 description,
                 completionStatus
             ) VALUES (
                 'Put cover sheet on TPS report',
                 0
             );'''
    c.execute(sql)


    conn.commit()
    conn.close()

    return databasePath

def printStatus(databasePath):
    conn = sqlite3.connect(databasePath)
    c = conn.cursor()

    # Create table
    sql = '''SELECT description FROM TodoTask WHERE completionStatus = 0;'''

    tasks = []
    for row in c.execute(sql):
        tasks.append(row[0])
    conn.commit()
    conn.close()

    today = datetime.date.today()

    print("")
    print( today.strftime("MFND - %B %d, %Y") )
    print("")

    num = len(tasks)
    if num != 0:
        for i in range(0, num):
            print("  " + str(i+1) + ". " + tasks[i]) 
        print("")

def getResponse():
    response = raw_input("> ")
    if (response == "exit"):
        print("MFND exiting...")
        return True

    return False

if  __name__ =='__main__':
    main()
