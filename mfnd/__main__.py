#!/usr/bin/env python3
"""

MFND - To-do list application

"""

import datetime
import os
from database import TodoDatabase
from parser import CommandParser


def main():

    # Initialize the database
    database = initDatabase()

    # While not done print status and get next input
    while (True):
        command = displayStatus(database)
        if (command.done):
            print("MFND exiting...")
            break
        updateStatus(command)

def initDatabase():
    """
    Initialize the to-do list database
    """

    scriptPath = os.path.dirname(os.path.realpath(__file__))
    databasePath = scriptPath + "/../data/todo_list.sqlite"

    database = TodoDatabase(databasePath)
    return database

def displayStatus(database):
    """
    Print the current state of the to-do list and get commands entered by user
    """

    today = datetime.date.today()
    print("")
    print( today.strftime("MFND - %B %d, %Y") )
    print("")

    tasks = database.getTasks()
    num = len(tasks)
    if num != 0:
        for i in range(0, num):
            print("  " + str(i+1) + ". " + tasks[i]) 
        print("")

    response = raw_input("> ")
    command = CommandParser(response)

    return command

def updateStatus(command):
    x = 0

if  __name__ =='__main__':
    main()
