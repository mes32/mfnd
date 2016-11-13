#!/usr/bin/env python3
"""

Module for input commands

"""

#from database import TodoDatabase 

def _printHelp():
    print("mfnd commands:")
    print("    exit                Exit from the program")
    print("    help                Display this help screen")
    print("    todo <description>  Add a new task with <description>")
    print("    done <number>       Mark the task at <number> as completed")

def _waitForUser():
    response = raw_input("> ")
    CommandParser(response).execute()

def tryAgain():
    _waitForUser()

def exitApplication():
    """
    Exit from the application
    """

    print("MFND exiting ...")
    quit()

def displayHelp():
    """
    Display program usage
    """

    _printHelp()
    _waitForUser()

def addTodoTask():
    """
    Add a new task to the to-do list
    """

    print("    # addTodoTask() - doing nothing")

def doneTodoTask():
    """
    Mark a task on the to-do list as done
    """

    print("    # doneTodoTask() - doing nothing")

def unusableCommand():
    """
    Display a warning about unusable command
    """

    _printHelp()
    print("")
    print("!!! Warning unusable input: ' '")
    _waitForUser()


class CommandParser:
    """
    Parse commands typed by the user to modify the to-do list
    """

    database = None
    @staticmethod
    def setDatabase(database):
        CommandParser.database = database

    functionDict = {
        'AGAIN'    : tryAgain,
        'EXIT'     : exitApplication,
        'HELP'     : displayHelp,
        'TODO'     : addTodoTask,
        'DONE'     : doneTodoTask,
        'UNUSABLE' : unusableCommand,
    }

    def __init__(self, line):
        """
        Parse a line and set values accordingly
        """

        tokens = line.split()
        if (tokens == []):
            self.function = self.functionDict['AGAIN']
        elif (tokens[0].lower() == "exit"):
            self.function = self.functionDict['EXIT']
        elif (tokens[0].lower() == "help"):
            self.function = self.functionDict['HELP']
        elif (tokens[0].lower() == "todo"):
            self.function = self.functionDict['TODO']
        else:
            self.function = self.functionDict['UNUSABLE']
            self.input = line

    def execute(self):
        self.function()

    def undo(self):
        print("    # undo() - doing nothing")

    def saveToDatabase(self):
        print("    # saveToDatabase() - doing nothing")

    def loadFromDatabase(self):
        print("    # loadFromDatabase() - doing nothing")
