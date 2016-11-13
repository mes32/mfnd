#!/usr/bin/env python3
"""

MFND - To-do list application

"""

import datetime
import os

from commands import CommandParser
from database import TodoDatabase
from todotask import TodoTask


def main():

    # Initialize the database
    database = initDatabase()
    printDB(database)
    CommandParser.setDatabase(database)

    # Program main loop (REPL)
    #   - Read commands from user
    #   - Evaluate commands updating database
    #   - Print current state of database
    #   - Loop until exit command 
    while (True):
        command = readCommand()
        evaluateCommand(command)
        printDB(database)

def initDatabase():
    """
    Initialize the to-do list database
    """

    scriptPath = os.path.dirname(os.path.realpath(__file__))
    databasePath = scriptPath + "/../data/todo_list.sqlite"

    database = TodoDatabase(databasePath)
    return database

def readCommand():
    """
    Read in new commands entered by the user
    """

    response = raw_input("> ")
    command = CommandParser(response)
    return command

def evaluateCommand(command):
    """
    Evaluate a previously read command to update the state of the to-do list
    """

    command.execute()

def printDB(database):
    """
    Print the current state of the to-do list
    """

    today = datetime.date.today()
    print("")
    print( today.strftime("MFND - %B %d, %Y") )
    print("")

    tasks = database.getTasks()
    num = len(tasks)
    if num != 0:
        for i in range(0, num):
            print('  {0}. {1}'.format(i+1, tasks[i]))
        print("")

if  __name__ =='__main__':
    main()
