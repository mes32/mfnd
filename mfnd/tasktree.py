#!/usr/bin/env python3
"""

Module for the to-do list tree

"""

from todotask import TodoTask 


class TaskTree:
    """
    Represents the to-do list and manages tree-like structure
    """

    def __init__(self):
        """
        Initialize a to-do list task tree
        """

        self.taskDict = dict()
        self.taskList = []

    def insert(self, rowid, parentID, task, maxDepth):
        """
        Insert a new task into the tree
        """
        node = TreeNode(parentID, task, maxDepth)

        self.taskDict[rowid] = node

        if parentID in self.taskDict:
            x = 0
            self.taskDict[parentID].addChild(node)

        self.taskList.append(task)

    def __str__(self):
        """
        Return a human readable str representation of this tree
        """

        outputStr = ""
        num = len(self.taskList)

        if num != 0:
            for i in self.taskDict:
                if self.taskDict[i].depth == 0:
                    outputStr += str(self.taskDict[i])

        return outputStr

class TreeNode:
    """
    Represents a single task in the to-do tree
    """

    def __init__(self, parentID, task, depth):
        """
        Initialize a to-do tree node
        """

        self.parentID = parentID
        self.task = task
        self.depth = depth

        self.children = []

    def addChild(self, node):
        """
        Add a child node to this node
        """

        self.children.append(node)

    def __str__(self):
        """
        Return a human readable str representation of this node
        """

        outputStr = ""
        outputStr += str(self.task) + "\n"
        for node in self.children:
            outputStr += "   " + str(node)

        return outputStr
