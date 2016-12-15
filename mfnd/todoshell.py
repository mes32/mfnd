#!/usr/bin/env python3
"""

Module defining a custom command shell

"""

import cmd
import datetime
import sys
import sqlite3

import cmdtoken
from database import TodoDatabase
from todotask import TodoTask
from tasktree import TaskTree


def printHelp():
    """
    Print a short help screen describing available commands
    """

    print("mfnd commands:")
    print("    exit               Exit from the program")
    print("    help               Display this help screen")
    print("    pumpkin <####>     Configure hour-of-day for reset of to-do list")
    print("                       Requires 4 digits in 24-hour clock mode (default 0400)")
    print("    undo               Undo previous command")
    print("    redo               Redo previous undone command")
    print()
    print("    todo <description>   Add a new task with <description>")
    print("    todosub <P> <description>  Add a sub-task under the task at position <P>")
    print("    done <P>           Mark the task at <P> as complete")
    print("    remove <P>         Delete the task at <P>")
    print()
    print("    move <P> up        Move task at <P> up one position")
    print("    move <P> down      Move task at <P> down one position")
    print("    move <P> top       Move task at <P> to top position")
    print("    move <P> bottom    Move task at <P> to bottom position")


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

        #completekey = 'tab'
        #stdin = None
        #stdout = None

        #super().__init__(completekey, stdin, stdout)
        super().__init__()
        self.database = database


    # ----- basic TodoShell commands -----
    def cmdloop(self):

        try:
            self.__printDB()
            super().cmdloop()
        except SystemExit:
            return
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def emptyline(self):
        """
        Entering an empty command just provides a fresh prompt
        """

    def default(self, line = None):
        """
        Display a warning about unusable command
        """

        printHelp()
        print()
        if line != None:
            print("!!! Warning unusable input: '" + line + "'")
        else:
            print("!!! Warning unusable input")

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

        description = arg
        print("In do_todo description = " + description)

        task = TodoTask(description)
        command = cmdtoken.TodoCommand(self.database, task)
        command.execute()

        self.__printDB()

    def do_todosub(self, arg):
        """
        Add a new sub-task under another task
        """

        tokens = arg.split()
        parentLabel = tokens[0]
        description = str(" ".join(tokens[1:]))

        task = TodoTask(description)
        self.database.insertTask(task, None, parentLabel)
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
        if len(tokens) != 2:
            self.default(self.lastcmd)
            return

        num = int(tokens[0])
        direction = tokens[1]

        if direction == 'up':
            self.database.moveUp(num)
        elif direction == 'down':
            self.database.moveDown(num)
        elif direction == 'top':
            self.database.moveTop(num)
        elif direction == 'bottom':
            self.database.moveBottom(num)
        else:
            self.default(self.lastcmd)
            return

        # except Exception:
        #     # In this case Exception is non-specific
        #     # The move could have failed due to other reasons
        #     self.default(self.lastcmd)
        #     return

        self.__printDB()

    def do_undo(self, arg):
        """
        Undo the last action
        """

        if cmdtoken.CommandStack.undo():
            self.__printDB()

    def do_redo(self, arg):
        """
        Redo the last undone action
        """
        
        if cmdtoken.CommandStack.redo():
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
            self.default()



    def __saveToDatabase(self):
        print("    # saveToDatabase() - doing nothing")

    def __loadFromDatabase(self):
        print("    # loadFromDatabase() - doing nothing")

    def __printDB(self):
        """
        Print the current state of the to-do list
        """

        today = datetime.date.today()
        print()
        print( today.strftime("MFND - %B %d, %Y") )
        print()

        tasks = self.database.getTasks()
        print(tasks)


