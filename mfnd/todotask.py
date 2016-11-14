#!/usr/bin/env python3
"""

Module for tasks in the to-do list

"""


class TodoTask:
    """
    Represents a task in the to-do list
    """

    def __init__(self, description, taskOrder = -1):
        """
        Initialize a to-do list task item
        """

        self.taskOrder = taskOrder
        self.description = description
        self.completionStatus = 0
        self.visible = True
        self.mode = 0

    def __str__(self):
        """
        Return a human readable str representation of this task
        """

        if self.completionStatus == 0:
            return "  " + str(self.taskOrder) + ". " + self.description
        elif self.completionStatus == 1:
            return "--- " + self.description + " ---"