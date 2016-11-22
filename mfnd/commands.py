#!/usr/bin/env python3
"""

Module for commands typed by the user

"""

import cmd, datetime, sys
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
    print("    remove <num>         Delete the task at <num>")
    print("    pumpkin <####>       Configure hour-of-day for reset of to-do list")
    print("                         Requires 4 digits in 24-hour clock mode (default 0400)")
    print("    move <num> up        Move task at <num> up one position")
    print("    //move <num> down      Move task at <num> down one position")
    print("    //move <num> top       Move task at <num> to top position")
    print("    //move <num> bottom    Move task at <num> to bottom position")


class TodoShell(cmd.Cmd):
    """
    Parse commands typed by the user to modify the to-do list
    """

    prompt = '> '
    file = None


    def __init__(self, database):
        """
        Initialize a shell for todo-list commands
        """

        completekey = 'tab'
        stdin = None
        stdout = None

        super().__init__(completekey, stdin, stdout)
        self.database = database


    # ----- basic TodoShell commands -----
    def cmdloop(self):

        self.__printDB()
        super().cmdloop()

    def emptyline(self):
        """
        Entering an empty command just provides a fresh prompt
        """

    def default(self, line):
        """
        Display a warning about unusable command
        """

        printHelp()
        print("")
        print("!!! Warning unusable input: '" + line + "'")

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
        self.__printDB()

    def do_done(self, arg):
        """
        Mark a task on the to-do list as done
        """

        self.database.doneTask(arg)
        self.__printDB()

    def do_remove(self, arg):
        """
        Delete a task from the to-do list
        """

        self.database.deleteTask(arg)
        self.__printDB()

    def do_pumpkin(self, arg):
        """
        Set the time at which the database will clear the to-do list
        """

        self.database.configurePumpkinTime(arg)
        self.__printDB()

    def do_move(self, arg):
        """
        Move a to-do task to another location in the list
        """

        tokens = arg.split()
        num = int(tokens[0])
        direction = tokens[1]

        if direction == "up":
            self.database.moveUp(num)
        elif direction == "down":
            self.database.moveDown(num)
        else:
            print("#    In do_move doing nothing")
        self.__printDB()

    def do_undo(self, arg):
        """
        Undo the last action
        """
        print("    # undo() - doing nothing")
        self.__printDB()

    def do_add(self, s):
        pass

    def complete_add(self, text, line, begidx, endidx):
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in completions if s.startswith(mline)]


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

    # ----- helper functions -----
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



    def __saveToDatabase(self):
        print("    # saveToDatabase() - doing nothing")

    def __loadFromDatabase(self):
        print("    # loadFromDatabase() - doing nothing")

    def __printDB(self):
        """
        Print the current state of the to-do list
        """

        today = datetime.date.today()
        print("")
        print( today.strftime("MFND - %B %d, %Y") )
        print("")

        tasks = self.database.getTasks()
        num = len(tasks)
        if num != 0:
            for i in range(0, num):
                print(tasks[i])
            print("")

