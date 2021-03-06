#!/usr/bin/env python3
"""

Module for the to-do list tree

"""

import copy

from todotask import TodoTask 


class TaskTree:
    """
    Represents the to-do list and manages tree-like structure
    """

    def __init__(self, database):
        """
        Initialize a to-do list task tree
        """

        # TODO: nodeTable should be indexed by label
        # Any functions that take rowid should take label

        self.database = database
        self.readDatabase()

    def readDatabase(self):

        self.nodeTable = dict()
        self.root = None
        self.mode = None
        self.database.initializeTaskTree(self)

    def insertTask(self, task, parentLabel=None):

        if parentLabel == None:
            parentID = self.mode.rowid
        else:
            parentID = self.lookupRowid(parentLabel)

        rowid = self.database.insertTask(task, parentID)
        self.readDatabase()
        label = self.lookupLabel(rowid)

        node = TreeNode(rowid, parentID, task)
        self.insertNode(node)

        return label

    def insertNode(self, node):
        """
        Insert a new task into the tree
        """

        if self.root == None:
            self.root = node
            node.depth = 0
        elif self.mode == None:
            # TODO: This would ideally be set elsewhere
            self.mode = node

        self.nodeTable[node.rowid] = node
        
        if node.parentID in self.nodeTable:
            self.nodeTable[node.parentID].addChild(node)
            node.depth = self.nodeTable[node.parentID].depth + 1

    def deleteTask(self, label):
        """
        Delete a task from the tree
        """

        rowid = self.lookupRowid(label)
        node = self.nodeTable[rowid]
        parentLabel = self.nodeTable[node.parentID].label
        trace = NodeTrace(node, parentLabel)

        self.database.deleteTask(rowid)

        return trace

    def insertTrace(self, nodeTrace):

        labelUnset = True

        for n in nodeTrace.list:
            node = n[0]
            label = n[1]
            
            currLabel = self.insertTask(node.task, label)

            if labelUnset:
                rootLabel = currLabel

        return rootLabel

    def lookupRowid(self, label):
        """
        Lookup a task's database rowid based on its label in the TaskTree
        """

        root = self.root
        rowid = root.lookupRowid(label)
        if rowid != -1:
            return rowid

        return -1

    def lookupLabel(self, rowid):
        """
        Lookup a task's label based on its rowid in the database
        """

        return self.nodeTable[rowid].label

    def setDone(self, label):
        """
        Mark the task at label as done
        """

        rowid = self.lookupRowid(label)
        self.database.updateCompletionStatus(rowid, TodoTask.TASK_DONE)

    def setUndone(self, label):
        """
        Mark the task at rowid as undone
        """

        rowid = self.lookupRowid(label)
        self.database.updateCompletionStatus(rowid, TodoTask.TASK_UNDONE)

    def moveTaskUp(self, label):
        """
        Move a task up one position
        """

        rowid = self.lookupRowid(label)
        trace = self.deleteTask(rowid)
        root = trace.list[0][0]

        if root.task.position > 1:
            root.task.position -= 1

        self.readDatabase()
        newLabel = self.insertTrace(trace)

        return newLabel

    def moveTaskDown(self, label):
        """
        Move a task down one position
        """

        rowid = self.lookupRowid(label)
        trace = self.deleteTask(rowid)
        root = trace.list[0][0]

        root.task.position += 1
        # TODO: Should check if at bottom already

        self.readDatabase()
        newLabel = self.insertTrace(trace)

        return newLabel

    def moveTask(self, label, position):
        """
        Move a task to a new position
        """

        print("label = " + label)
        print("position = " + str(position))


        rowid = self.lookupRowid(label)
        trace = self.deleteTask(rowid)
        root = trace.list[0][0]

        oldPosition = root.task.position
        root.task.position = position

        self.readDatabase()
        newLabel = self.insertTrace(trace)
        self.readDatabase()

        print("newLabel = " + newLabel)
        print("oldPosition = " + str(oldPosition))

        return (newLabel, oldPosition)

    def __str__(self):
        """
        Return a human readable str representation of this tree
        """

        self.readDatabase()

        if self.root == None:
            return "[Empty Task Tree]"
        else:
            return self.mode.toString()

class TreeNode:
    """
    Represents a single task in the to-do tree
    """

    def __init__(self, rowid, parentID, task, depth=0):
        """
        Initialize a to-do tree node
        """

        self.label = ""
        self.rowid = rowid
        self.parentID = parentID
        self.depth = depth

        self.task = task
        self.children = []

    def addChild(self, childNode):
        """
        Add a child node to this node
        """

        self.children.append(childNode)

        if self.depth > 0:
            if self.depth == 2:
                childNode.label = self.label + TreeNode.__charPos(childNode.task.position) + "."
            else:
                childNode.label = self.label + str(childNode.task.position) + "."

    def __str__(self):
        return "[-- TreeNode --]"

    def lookupRowid(self, label):
        """
        Lookup a task's database rowid based on its label in the TaskTree
        """

        if self.label[:-1] == label or self.label == label:
            return self.rowid

        for childNode in self.children:
            rowid = childNode.lookupRowid(label)
            if rowid != -1:
                return rowid

        return -1

    def toString(self, level=0):
        """
        Return a human readable str representation of this node
        """

        outputStr = "  " * level

        if level > 0:
            if self.task.completionStatus == TodoTask.TASK_DONE:
                outputStr += "--- " + self.task.description + " ---\n"
            else:
                outputStr += " " + self.label + " " + self.task.description + "\n"

        for node in self.children:
            outputStr += node.toString(level + 1)

        return outputStr

    def __charPos(position):
        num = position - 1

        if num < 0:
            return ""

        outputStr = ""
        outputStr += chr(num % 26 + 97)
        num = int(num / 26)
        outputStr = TreeNode.__charPos(num) + outputStr

        return outputStr

class NodeTrace:

    def __init__(self, root, parentLabel):

        self.root = root
        self.list = list()
        self.add(root, parentLabel)

    def add(self, node, label):

        copyNode = copy.deepcopy(node)
        if label == "":
            label = None   
        self.list.append( (copyNode, label) )

        label = node.label
        for childNode in node.children:
            self.add(childNode, label)

