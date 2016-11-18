#!/usr/bin/env python3
"""

Module for commands typed by the user

"""

import cmd, sys
import sqlite3

from database import TodoDatabase
from todotask import TodoTask
from turtle import *


def printHelp():
    """
    Print a short help screen describing available commands
    """

    print("mfnd commands:")
    print("    exit                 Exit from the program")
    print("    help                 Display this help screen")
    print("    todo <description>   Add a new task with <description>")
    print("    done <num>           Mark the task at <num> as completed")
    print("    remove <num>         Delete the task at <num>")
    print("    pumpkin <####>       Configure hour-of-day for reset of to-do list")
    print("                         Requires 4 digits in 24-hour clock mode (default 0400)")
    print("    //move <num> up        Move task at <num> up one position")
    print("    //move <num> down      Move task at <num> down one position")
    print("    //move <num> top       Move task at <num> to top position")
    print("    //move <num> bottom    Move task at <num> to bottom position")


# def readNext():
#     """
#     Read in and return the next command typed by the user
#     """

#     response = input("> ")
#     command = CommandParser(response)
#     return command


class TodoShell(cmd.Cmd):
    """
    Parse commands typed by the user to modify the to-do list
    """

    intro = 'Welcome to TodoShell.   Type help or ? to list commands.\n'
    prompt = '> '
    file = None

    database = None
    @staticmethod
    def setDatabase(database):
        TodoShell.database = database

    # def __init__(self, line):
    #     """
    #     Parse a line and set values accordingly
    #     """

    #     self.line = line

    #     commandPayload = ""
    #     onFirstSpace = line.strip().split(None, 1)
    #     if len(onFirstSpace) > 1:
    #         commandPayload = onFirstSpace[1]

    #     tokens = line.split()




    #     elif tokens[0].lower() == "todo" and len(commandPayload) > 0:
    #         self.todoDescription = commandPayload
    #         self.executeFunc = self.__addTodoTask

    #     elif tokens[0].lower() == "done" and commandPayload.isdigit():
    #         self.donePosition = commandPayload
    #         self.executeFunc = self.__doneTodoTask

    #     elif tokens[0].lower() == "remove" and commandPayload.isdigit():
    #         self.removePosition = commandPayload
    #         self.executeFunc = self.__removeTodoTask

    #     elif tokens[0].lower() == "pumpkin" and commandPayload.isdigit():
    #         self.pumpkinTime = commandPayload
    #         self.executeFunc = self.__setPumpkinTime 

    #     else:
    #         self.executeFunc = self.__unusableCommand


# todo done done remove pumpkin

    # ----- basic TodoShell commands -----
    def do_exit(self, arg):
        """
        Exit from the application
        """

        print("MFND exiting ...")
        self.close()
        exit()

        return True

    def do_help(self, arg):
        """
        Display program usage
        """

        printHelp()

    def do_todo(self, arg):
        """
        Add a new task to the to-do list
        """

        task = TodoTask(arg)
        self.database.insertTask(task)

    def do_left(self, arg):
        'Turn todo left by given number of degrees:  LEFT 90'
        left(*parse(arg))
    def do_goto(self, arg):
        'Move todo to an absolute position with changing orientation.  GOTO 100 200'
        goto(*parse(arg))
    def do_home(self, arg):
        'Return todo to the home position:  HOME'
        home()
    def do_circle(self, arg):
        'Draw circle with given radius an options extent and steps:  CIRCLE 50'
        circle(*parse(arg))
    def do_position(self, arg):
        'Print the current turle position:  POSITION'
        print('Current position is %d %d\n' % position())
    def do_heading(self, arg):
        'Print the current turle heading in degrees:  HEADING'
        print('Current heading is %d\n' % (heading(),))
    def do_color(self, arg):
        'Set the color:  COLOR BLUE'
        color(arg.lower())
    def do_undo(self, arg):
        'Undo (repeatedly) the last turtle action(s):  UNDO'
    def do_reset(self, arg):
        'Clear the screen and return turtle to center:  RESET'
        reset()

    # ----- record and playback -----
    def do_record(self, arg):
        'Save future commands to filename:  RECORD rose.cmd'
        self.file = open(arg, 'w')
    def do_playback(self, arg):
        'Playback commands from a file:  PLAYBACK rose.cmd'
        self.close()
        with open(arg) as f:
            self.cmdqueue.extend(f.read().splitlines())
    def precmd(self, line):
        line = line.lower()
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line
    def close(self):
        if self.file:
            self.file.close()
            self.file = None




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

        self.database.doneTask(self.donePosition)

    def __removeTodoTask(self):
        """
        Delete a task from the to-do list
        """

        self.database.deleteTask(self.removePosition)

    def __setPumpkinTime(self):
        """
        Set the reset time
        """

        self.database.configurePumpkinTime(self.pumpkinTime)


    def __unusableCommand(self):
        """
        Display a warning about unusable command
        """

        printHelp()
        print("")
        print("!!! Warning unusable input: '" + self.line + "'")
        self = readNext()
        self.execute()

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    print("--- In parse() ---")
    a = arg.split()
    print("a = " + str(a))
    m = map(int, a)
    print("m = " + str(m))
    t = tuple(m)
    print("t = " + str(t))
    print("--- ---")
    return t
