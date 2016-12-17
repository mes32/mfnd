#!/usr/bin/env python3
"""

Module defining a custom command shell for mfnd

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

        completekey = 'tab'
        stdin = None
        stdout = None

        super().__init__(completekey, stdin, stdout)

        self.database = database
        cmdtoken.CommandStack.setDatabase(database)

    def cmdloop(self):
        """
        Run command loop REPL until the user exits
        """

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
        Entering an empty command just provides a blank prompt
        """

    def default(self, line=None):
        """
        Print help screen and display a warning about the unusable command
        """

        printHelp()
        print()

        if line != None:
            print("!!! Warning unusable input: '" + line + "'")
        else:
            print("!!! Warning unusable input")

    def do_exit(self, arg):
        """
        Exit from the command shell and the program
        """

        print("MFND exiting ...")
        self.close()
        exit()

        return True

    def do_help(self, arg):
        """
        Display program usage help screen
        """

        printHelp()

    def do_todo(self, arg):
        """
        Add a new task to the to-do list
        """

        description = arg
        task = TodoTask(description)
        command = cmdtoken.TodoCommand(task)
        command.execute()

        self.__printDB()

    def do_todosub(self, arg):
        """
        Add a new sub-task to the to-do list under another task
        """

        tokens = arg.split()
        parentLabel = tokens[0]
        description = str(" ".join(tokens[1:]))

        task = TodoTask(description)
        command = cmdtoken.TodosubCommand(task, parentLabel)
        command.execute()

        self.__printDB()   

    def do_done(self, arg):
        """
        Mark a task in the to-do list as done
        """

        label = arg
        command = cmdtoken.DoneCommand(label)
        command.execute()   

        self.__printDB()

    def do_remove(self, arg):
        """
        Delete a task from the to-do list
        """

        label = arg
        command = cmdtoken.RemoveCommand(label)
        command.execute()

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

        label = int(tokens[0])
        direction = tokens[1]

        if direction == 'up':
            self.database.moveUp(label)
        elif direction == 'down':
            self.database.moveDown(label)
        elif direction == 'top':
            self.database.moveTop(label)
        elif direction == 'bottom':
            self.database.moveBottom(label)
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
        Undo the last successful command if possible
        """

        if cmdtoken.CommandStack.undo():
            self.__printDB()

    def do_redo(self, arg):
        """
        Redo the last undone command if possible
        """

        if cmdtoken.CommandStack.redo():
            self.__printDB()

    def do_add(self, s):
        pass

    def complete_add(self, text, line, begidx, endidx):
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in completions if s.startswith(mline)]

    def do_record(self, arg):
        """
        Save future commands to filename:  RECORD rose.cmd
        """

        self.file = open(arg, 'w')

    def do_playback(self, arg):
        """
        Playback commands from a file:  PLAYBACK rose.cmd
        """

        self.close()
        with open(arg) as f:
            self.cmdqueue.extend(f.read().splitlines())

    def precmd(self, line):

        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line

    def close(self):

        if self.file:
            self.file.close()
            self.file = None

    def execute(self):
        """
        Execute the current command if possible
        """

        try:
            self.executeFunc()
        except SystemExit:
             sys.exit(0)
        except sqlite3.Error as err:
            print("Check 'database' module. Caught SQLite exception: " + err.args[0])
            sys.exit(1)
        except:
            self.default()

    def __saveHistory(self):
        """
        Save command history to the database so it can be loaded for later sessions
        """

        print("    # In TodoShell __saveHistory() - doing nothing")

    def __loadHistory(self):
        """
        Load command history from the database saved during previous sessions
        """

        print("    # In TodoShell __loadHistory() - doing nothing")

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


