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

    stack = list()
    stackIndex = 0
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

        CommandStack.stackIndex += 1

        if inredo == False:
            CommandStack.stack.insert(CommandStack.stackIndex - 1, token)
            CommandStack.maxIndex = CommandStack.stackIndex

    @staticmethod
    def pop():
        """
        Remove a command token from the top of the stack and return
        """

        token = CommandStack.stack[CommandStack.stackIndex - 1]
        CommandStack.stackIndex -= 1

        return token

    @staticmethod
    def undo():
        """
        Roll back the previous command
        """

        if CommandStack.stackIndex == 0:
            return False
        else:
            CommandStack.pop().undo()            
            return True

    @staticmethod
    def redo():
        """
        Go forward from a previously undone command if possible
        """

        if CommandStack.stackIndex == CommandStack.maxIndex:
            return False
        else:
            CommandStack.stack[CommandStack.stackIndex].execute(True)
            return True

class TodoCommand:
    """
    Class for command 'todo'
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
    Class for command 'todosub'
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
    Class for command 'done'
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