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

        self.tasks = []

    def insert(self, rowid, parentID, task, maxDepth):
        """
        Insert a new task into the tree
        """
        self.tasks.append(task)

    def __str__(self):
        """
        Return a human readable str representation of this tree
        """

        outputStr = ""
        num = len(self.tasks)

        if num != 0:
            for i in range(0, num):
                outputStr += str(self.tasks[i]) + "\n"
            outputStr += "\n"

        return outputStr