#!/usr/bin/env python3
"""

Module for input commands

"""

#from database import TodoDatabase 

def printHelp():
    print("mfnd commands:")
    print("    exit                Exit from the program")
    print("    help                Display this help screen")
    print("    todo <description>  Add a new task with <description>")
    print("    done <number>       Mark the task at <number> as completed")

def waitForUser():
    response = raw_input("> ")
    CommandParser(response).execute()


class CommandParser:
    """
    Parse commands typed by the user to modify the to-do list
    """

    database = None
    @staticmethod
    def setDatabase(database):
        CommandParser.database = database

    def __init__(self, line):
        """
        Parse a line and set values accordingly
        """

        tokens = line.split()
        if (tokens == []):
            self.executeFunc = self.__tryAgain
        elif (tokens[0].lower() == "exit"):
            self.executeFunc = self.__exitApplication
        elif (tokens[0].lower() == "help"):
            self.executeFunc = self.__displayHelp
        elif (tokens[0].lower() == "todo"):
            self.executeFunc = self.__addTodoTask
        else:
            self.executeFunc = self.__unusableCommand
            self.input = line

    def execute(self):
        self.executeFunc()

    def undo(self):
        print("    # undo() - doing nothing")

    def saveToDatabase(self):
        print("    # saveToDatabase() - doing nothing")

    def loadFromDatabase(self):
        print("    # loadFromDatabase() - doing nothing")

    def __tryAgain(self):
        waitForUser()

    def __exitApplication(self):
        """
        Exit from the application
        """

        print("MFND exiting ...")
        quit()

    def __displayHelp(self):
        """
        Display program usage
        """

        printHelp()
        waitForUser()

    def __addTodoTask(self):
        """
        Add a new task to the to-do list
        """

        print("    # addTodoTask() - doing nothing")

    def __doneTodoTask(self):
        """
        Mark a task on the to-do list as done
        """

        print("    # doneTodoTask() - doing nothing")

    def __unusableCommand(self):
        """
        Display a warning about unusable command
        """

        printHelp()
        print("")
        print("!!! Warning unusable input: ' '")
        waitForUser()

