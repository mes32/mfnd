#!/usr/bin/env python3
"""

MFND - To-do list application

"""

import os

import commands
from commands import TodoShell
from database import TodoDatabase
from todotask import TodoTask


def main():

    # Initialize the database
    database = initDatabase()

    # Program main loop (REPL)
    #   - Read commands from user
    #   - Evaluate commands updating database
    #   - Print current state of database
    #   - Loop until exit command 
    TodoShell(database).cmdloop()


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

    return commands.readNext()

def evaluateCommand(command):
    """
    Evaluate a previously read command to update the state of the to-do list
    """

    command.execute()

if  __name__ =='__main__':
    main()
