#!/usr/bin/env python3
"""

Module for input commands

"""

#from database import TodoDatabase 

def exitApplication():
    """
    Exit from the application
    """

    print("MFND exiting ...")
    quit()

def _printHelp():
    print("    # _printHelp() - doing nothing")

def displayHelp():
    """
    Display program usage
    """

    _printHelp()
    print("    # displayHelp() - doing nothing")

def addTodoTask():
    """
    Add a new task to the to-do list
    """

    print("    # addTodoTask() - doing nothing")

def unusableCommand():
    """
    Display a warning about unusable command
    """

    _printHelp()
    print("    # unusableCommand() - doing nothing")


class CommandParser:
    """
    Parse commands typed by the user to modify the to-do list
    """

    database = None
    @staticmethod
    def setDatabase(database):
        CommandParser.database = database

    functionDict = {
        'EXIT'     : exitApplication,
        'HELP'     : displayHelp,
        'TODO'     : addTodoTask,
        'UNUSABLE' : unusableCommand,
    }

    def __init__(self, line):
        """
        Parse a line and set values accordingly
        """

        tokens = line.split()
        if (tokens[0].lower() == "exit"):
            self.function = self.functionDict['EXIT']
        elif (tokens[0].lower() == "help"):
            self.function = self.functionDict['HELP']
        elif (tokens[0].lower() == "todo"):
            self.function = self.functionDict['TODO']
        else:
            self.function = self.functionDict['UNUSABLE']

    def execute(self):
        self.function()

    def undo(self):
        print("    # undo() - doing nothing")