#!/usr/bin/env python3
"""

Module defining command tokens (Command Pattern) for use by the TodoShell CLI

"""

from database import TodoDatabase
from todotask import TodoTask


class CommandStack:
    """
    Stack of command tokens that can be navigated forward and backward with undo/redo
    """

    stack = list()
    nextIndex = 0
    maxIndex = 0

    @staticmethod
    def setDatabase(database):
        """
        Set the database on which commands will act
        """

        CommandStack.database = database

    @staticmethod
    def push(token, inredo):
        """
        Add a new command token to the top of the stack
        """

        CommandStack.nextIndex += 1

        if inredo == False:
            CommandStack.stack.insert(CommandStack.nextIndex - 1, token)
            CommandStack.maxIndex = CommandStack.nextIndex

    @staticmethod
    def pop():
        """
        Remove a command token from the top of the stack and return it
        """

        token = CommandStack.stack[CommandStack.nextIndex - 1]ne
        CommandStack.nextIndex -= 1

        return token

    @staticmethod
    def undo():
        """
        Roll back the previous command if possible. Return 'True' if possible.
        """

        if CommandStack.nextIndex == 0:
            return False
        else:
            CommandStack.pop().undo()            
            return True

    @staticmethod
    def redo():
        """
        Go forward from a previously undone command if possible. Return 'True' if possible.
        """

        if CommandStack.nextIndex == CommandStack.maxIndex:
            return False
        else:
            CommandStack.stack[CommandStack.nextIndex].execute(True)
            return True

class TodoCommand:
    """
    Class for 'todo' commands in todoshell
    """

    def __init__(self, task):

        self.task = task

    def execute(self, inredo=False):
        """
        Execute this command
        """

        self.rowid = CommandStack.database.insertTask(self.task)
        CommandStack.push(self, inredo)

    def undo(self):
        """
        Undo this command
        """

        CommandStack.database.deleteTask(None, self.rowid)

class TodosubCommand:
    """
    Class for 'todosub' commands in todoshell
    """

    def __init__(self, task, parentLabel):

        self.task = task
        self.parentLabel = parentLabel

    def execute(self, inredo=False):
        """
        Execute this command
        """

        self.rowid = CommandStack.database.insertTask(self.task, None, self.parentLabel)

        CommandStack.push(self, inredo)

    def undo(self):
        """
        Undo this command
        """

        CommandStack.database.deleteTask(None, self.rowid)

class DoneCommand:
    """
    Class for 'done' commands in todoshell
    """

    def __init__(self, label):

        self.label = label

    def execute(self, inredo=False):
        """
        Execute this command
        """

        self.rowid = CommandStack.database.doneTask(self.label)
        CommandStack.push(self, inredo)

    def undo(self):
        """
        Undo this command
        """

        CommandStack.database.todoTask(self.rowid)

class RemoveCommand:
    """
    Class for 'remove' commands in todoshell
    """

    def __init__(self, label):

        self.label = label

    def execute(self, inredo=False):
        """
        Execute this command
        """

        self.tree = CommandStack.database.deleteTask(self.label)
        CommandStack.push(self, inredo)

    def undo(self):
        """
        Undo this command
        """

        CommandStack.database.insertTree(self.tree)