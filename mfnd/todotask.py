#!/usr/bin/env python3
"""

Module for tasks in the to-do list

"""


class TodoTask:
    """
    Represents a task in the to-do list
    """

    def __init__(self, description, position = None, completionStatus = 'todo'):
        """
        Initialize a to-do list task item
        """

        self.description = description
        self.position = position
        self.completionStatus = completionStatus
        self.visible = True
        self.mode = 0

    def __str__(self):
        """
        Return a human readable str representation of this task
        """

        if self.completionStatus == 'todo':
            return "  " + str(self.position) + ". " + self.description
        elif self.completionStatus == 'done':
            return " --- " + self.description + " ---"