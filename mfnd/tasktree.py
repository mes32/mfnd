#!/usr/bin/env python3
"""

Module for the to-do list tree

"""

from todotask import TodoTask 


class TaskTree:
    """
    Represents the to-do list and manages tree-like structure
    """

    TASK_DONE = 'done'
    TASK_UNDONE = 'todo'

    def __init__(self, database):
        """
        Initialize a to-do list task tree
        """

        self.nodeTable = dict()
        self.root = None
        self.mode = None
        self.database = database
        self.database.initializeTaskTree(self)

    def insertTask(self, task, parentLabel=None, parentID=None):

        if parentID == None:
            if parentLabel == None:
                parentID = self.mode.rowid
            else:
                parentID = self.lookupRowid(parentLabel)

        rowid = self.database.insertTask(task, parentID)
        node = TreeNode(rowid, parentID, task)
        self.insertNode(node)

        return rowid

    def insertSubtree(self, subtree):
        parentID = subtree.root.parentID
        self.__recusiveInsertTree(subtree.root, parentID)

    def __recusiveInsertTree(self, node, parentID):
        task = node.task
        self.insertTask(node.task, None, parentID)

        rowid = node.rowid
        for childNode in node.children:
            self.__recusiveInsertTree(childNode, rowid)

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

    def deleteNode(self, rowid):
        """
        Delete a task from the tree
        """

        subtree = self.__getSubtree(rowid)
        print("deleteNode()")

        node = self.nodeTable[rowid]
        parentID = node.parentID
        parentNode = self.nodeTable[parentID]
        parentNode.children.remove(node)

        for childNode in self.nodeTable[rowid].children:
            deleteNode(childNode.rowid)

        del self.nodeTable[rowid]

        self.database.deleteTask(rowid)

        return subtree

    def lookupRowid(self, label):
        """
        Lookup a task's database rowid based on its label in the TaskTree
        """

        root = self.root
        rowid = root.lookupRowid(label)
        if rowid != -1:
            return rowid

        return -1

    def __getSubtree(self, rootID):
        """
        Return a sub-tree of this tree based on the root node's rowid
        """

        root = self.nodeTable[rootID]
        subtree = TaskTree(self.database)
        subtree.__recursiveCopy(root)
        return subtree

    def __recursiveCopy(self, node):
        print("__recursiveCopy() " + node.task.description)
        copyNode = node.copy()
        self.insertNode(copyNode)

        for childNode in node.children:
            self.__recursiveCopy(childNode)

    def setDone(self, rowid):
        """
        Mark the task at rowid as done
        """

        node = self.nodeTable[rowid]
        node.task.completionStatus = TaskTree.TASK_DONE
        self.database.updateCompletionStatus(rowid, node.task.completionStatus)

    def setUndone(self, rowid):
        """
        Mark the task at rowid as undone
        """

        node = self.nodeTable[rowid]
        node.task.completionStatus = TaskTree.TASK_UNDONE
        self.database.updateCompletionStatus(rowid, node.task.completionStatus)

    def __str__(self):
        """
        Return a human readable str representation of this tree
        """

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

    def copy(self):

        copyNode = TreeNode(self.rowid, self.parentID, self.task, self.depth)
        return copyNode


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
            if self.task.completionStatus == TaskTree.TASK_DONE:
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
