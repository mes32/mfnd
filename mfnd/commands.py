#!/usr/bin/env python3
"""

Module for commands typed by the user

"""

from database import TodoDatabase
from todotask import TodoTask


def printHelp():
    print("mfnd commands:")
    print("    exit                Exit from the program")
    print("    help                Display this help screen")
    print("    todo <description>  Add a new task with <description>")
    print("    done <number>       Mark the task at <number> as completed")

def readNext():
    response = raw_input("> ")
    command = CommandParser(response)
    return command


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
        if len(tokens) == 0:
            self.executeFunc = self.__tryAgain

        elif tokens[0].lower() == "exit":
            self.executeFunc = self.__exitApplication

        elif tokens[0].lower() == "help":
            self.executeFunc = self.__displayHelp

        elif tokens[0].lower() == "todo" and len(tokens) > 1:
            splitList = line.strip().split(None, 1)
            self.todoDescription = splitList[1]
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
        """
        Read in another command and evaluated it (i.e. let the user try again)
        """

        command = readNext()
        command.execute()

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
        command = readNext()
        command.execute()

    def __addTodoTask(self):
        """
        Add a new task to the to-do list
        """
        
        task = TodoTask(self.todoDescription)
        self.database.insertTask(task)

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
        command = readNext()
        command.execute()
