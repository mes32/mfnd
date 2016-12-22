#!/usr/bin/env python3
"""

Module defining command tokens (Command Pattern) for use by the TodoShell CLI

"""

from todotask import TodoTask


class CommandStack:
    """
    Stack of command tokens that can be navigated forward and backward with undo/redo
    """

    stack = list()
    nextIndex = 0
    maxIndex = 0

    @staticmethod
    def setTaskTree(taskTree):
        """
        Set the database on which commands will act
        """

        CommandStack.taskTree = taskTree

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

        token = CommandStack.stack[CommandStack.nextIndex - 1]
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

        self.rowid = CommandStack.taskTree.insertTask(self.task)
        CommandStack.push(self, inredo)

    def undo(self):
        """
        Undo this command
        """

        CommandStack.taskTree.deleteTask(self.rowid)

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

        self.rowid = CommandStack.taskTree.insertTask(self.task, self.parentLabel)
        CommandStack.push(self, inredo)

    def undo(self):
        """
        Undo this command
        """

        CommandStack.taskTree.deleteTask(self.rowid)

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

        self.rowid = CommandStack.taskTree.lookupRowid(self.label)
        CommandStack.taskTree.setDone(self.rowid)
        CommandStack.push(self, inredo)

    def undo(self):
        """
        Undo this command
        """

        CommandStack.taskTree.setUndone(self.rowid)

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

        self.rowid = CommandStack.taskTree.lookupRowid(self.label)
        self.trace = CommandStack.taskTree.deleteTask(self.rowid)
        CommandStack.push(self, inredo)

    def undo(self):
        """
        Undo this command
        """

        CommandStack.taskTree.insertTrace(self.trace)

class MoveUpCommand:
    """
    Class for 'move up' commands in todoshell
    """

    def __init__(self, label):

        self.label = label

    def execute(self, inredo=False):
        """
        Execute this command
        """

        self.newLabel = CommandStack.taskTree.moveTaskUp(self.label)
        CommandStack.push(self, inredo)

    def undo(self):
        """
        Undo this command
        """

        CommandStack.taskTree.moveTaskDown(self.newLabel)

class MoveDownCommand:
    """
    Class for 'move down' commands in todoshell
    """

    def __init__(self, label):

        self.label = label

    def execute(self, inredo=False):
        """
        Execute this command
        """

        self.newLabel = CommandStack.taskTree.moveTaskDown(self.label)
        CommandStack.push(self, inredo)

    def undo(self):
        """
        Undo this command
        """

        CommandStack.taskTree.moveTaskUp(self.newLabel)

class MoveTopCommand:
    """
    Class for 'move top' commands in todoshell
    """

    def __init__(self, label):

        self.label = label

    def execute(self, inredo=False):
        """
        Execute this command
        """

        (self.newLabel, self.oldPosition) = CommandStack.taskTree.moveTask(self.label, 1)
        CommandStack.push(self, inredo)

    def undo(self):
        """
        Undo this command
        """

        CommandStack.taskTree.moveTask(self.newLabel, self.oldPosition)

class MoveBottomCommand:
    """
    Class for 'move bottom' commands in todoshell
    """

    def __init__(self, label):

        self.label = label

    def execute(self, inredo=False):
        """
        Execute this command
        """

        # self.newLabel = CommandStack.taskTree.moveTaskBottom(self.label)
        # CommandStack.push(self, inredo)

    def undo(self):
        """
        Undo this command
        """