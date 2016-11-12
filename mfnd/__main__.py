#!/usr/bin/env python3
"""

MFND - To-do list application

"""

import datetime
import os
from database import TodoDatabase


def main():

    # Initialize the database
    database = initDatabase()

    # While not done print status and get next input
    done = False
    while (not done):
        done = displayStatus(database)


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
    tasks = database.getTasks()

    print("")
    print( today.strftime("MFND - %B %d, %Y") )
    print("")

    num = len(tasks)
    if num != 0:
        for i in range(0, num):
            print("  " + str(i+1) + ". " + tasks[i]) 
        print("")

    response = raw_input("> ")
    if (response == "exit"):
        print("MFND exiting...")
        return True

    return False


if  __name__ =='__main__':
    main()
