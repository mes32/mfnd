#!/usr/bin/env python3
"""

Module for commands typed by the user

"""

import sys
import sqlite3

from database import TodoDatabase
from todotask import TodoTask


def printHelp():
    """
    Print a short help screen describing available commands
    """

    print("mfnd commands:")
    print("    exit                 Exit from the program")
    print("    help                 Display this help screen")
    print("    todo <description>   Add a new task with <description>")
    print("    done <num>           Mark the task at <num> as completed")
    print("    //move <num> up        Move task at <num> up one position")
    print("    //move <num> down      Move task at <num> down one position")
    print("    //move <num> top       Move task at <num> to top position")
    print("    //move <num> bottom    Move task at <num> to bottom position")


def readNext():
    """
    Read in and return the next command typed by the user
    """

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

        self.line = line

        commandPayload = ""
        onFirstSpace = line.strip().split(None, 1)
        if len(onFirstSpace) > 1:
            commandPayload = onFirstSpace[1]

        tokens = line.split()

        if len(tokens) == 0:
            self.executeFunc = self.__tryAgain

        elif tokens[0].lower() == "exit":
            self.executeFunc = self.__exitApplication

        elif tokens[0].lower() == "help":
            self.executeFunc = self.__displayHelp

        elif tokens[0].lower() == "todo" and len(commandPayload) > 0:
            self.todoDescription = commandPayload
            self.executeFunc = self.__addTodoTask

        elif tokens[0].lower() == "done" and commandPayload.isdigit():
            self.donePosition = commandPayload
            self.executeFunc = self.__doneTodoTask

        else:
            self.executeFunc = self.__unusableCommand

    def execute(self):
        try:
            self.executeFunc()
        except SystemExit:
             sys.exit(0)
        except sqlite3.Error as err:
            print("Check 'database' module. Caught SQLite exception: " + err.args[0])
            sys.exit(1)
        except:
            self.__unusableCommand()

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

        self = readNext()
        self.execute()

    def __exitApplication(self):
        """
        Exit from the application
        """

        print("MFND exiting ...")
        sys.exit(0)

    def __displayHelp(self):
        """
        Display program usage
        """

        printHelp()
        self = readNext()
        self.execute()

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

        #self.database.doneTask(self.donePosition)


    def __unusableCommand(self):
        """
        Display a warning about unusable command
        """

        printHelp()
        print("")
        print("!!! Warning unusable input: '" + self.line + "'")
        self = readNext()
        self.execute()
