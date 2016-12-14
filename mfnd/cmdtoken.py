#!/usr/bin/env python3
"""

Module defining command tokens (Command Pattern) for use by the TodoShell CLI

"""

from database import TodoDatabase
from todotask import TodoTask


class CommandStack:
    """
    Stack of command tokens that can be navigated forward and backward
    """

    def push(self, token):
        """
        Add a new command token to the top of the stack
        """

    def pop(self):
        """
        Remove a command token from the top of the stack and return
        """

    def undo(self):
        """
        Roll back the previous command
        """

    def redo(self):
        """
        Go forward from a previously undone command if possible
        """

class TodoCommand:
    """
    Class for command 'todo'
    """

    def __init__(self, database, task):

        self.database = database
        self.task = task

    def execute(self):
        """
        Execute this command
        """

        self.rowid = self.database.insertTask(self.task)


    def undo(self):
        """
        Undo this command
        """

        self.database.deleteTask(None, self.rowid)