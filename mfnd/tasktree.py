#!/usr/bin/env python3
"""

Module for the to-do list tree

"""

import re

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

        node = TreeNode(rowid, parentID, task, maxDepth)
        self.taskDict[rowid] = node
        if parentID in self.taskDict:
            self.taskDict[parentID].addChild(node)

        self.taskList.append(task)

    def getRowid(self, treeLabel):
        """
        Lookup a task's database rowid based on its label in the TaskTree
        """

        positionList = treeLabel.split(".")
        position = int(positionList[0])
        suffix = ".".join(positionList[1:])

        num = len(self.taskDict)

        if num == 0:
            return -1

        for i in self.taskDict:
            if self.taskDict[i].depth == 2 and position == self.taskDict[i].task.position:
                if suffix == "":
                    return self.taskDict[i].rowid
                else:
                    return self.taskDict[i].getRowid(suffix)

        return -1


    def __str__(self):
        """
        Return a human readable str representation of this tree
        """

        outputStr = ""
        num = len(self.taskDict)

        count = 1

        if num != 0:
            for i in self.taskDict:
                if self.taskDict[i].depth == 2:
                    outputStr += self.taskDict[i].formatStr(count)
                    count += 1

        return outputStr

class TreeNode:
    """
    Represents a single task in the to-do tree
    """

    def __init__(self, rowid, parentID, task, depth):
        """
        Initialize a to-do tree node
        """

        self.rowid = rowid
        self.parentID = parentID
        self.task = task
        self.depth = depth

        self.children = []

    def addChild(self, node):
        """
        Add a child node to this node
        """

        self.children.append(node)

    def getRowid(self, treeLabel):
        """
        Lookup a task's database rowid based on its label in the TaskTree
        """

        if treeLabel == "":
            return self.rowid

        positionList = treeLabel.split(".")
        if self.depth == 2:
            # TODO: Should reverse multi-letter indexes
            position = ord(positionList[0]) - 96
        else:
            position = int(positionList[0])
        suffix = ".".join(positionList[1:])

        return self.children[position - 1].getRowid(suffix)

    def formatStr(self, count = 1, parentLabel = ""):
        """
        Return a human readable str representation of this node
        """

        if self.depth == 3:
            # TODO: Should wrap to more than one digit for 'count' > 122
            label = "   " + parentLabel + chr(count + 96) + "."
        else:
            label = "   " + parentLabel + str(count) + "."

        if self.task.completionStatus == 'done':
            labelRegex = re.compile(r'[0-9\.a-z]|[ ](?=[0-9])')
            newLabel = re.sub(labelRegex, '-', label)
            outputStr = newLabel + " " + str(self.task) + " ---\n"
        else:
            outputStr = label + " " + str(self.task) + "\n"

        count = 1
        for node in self.children:
            outputStr += node.formatStr(count, label)
            count += 1

        return outputStr
