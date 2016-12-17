#!/usr/bin/env python3
"""

Module handles tasks in the to-do list

"""


class TodoTask:
    """
    Class represents a task in the to-do list
    """

    def __init__(self, description, position = None, completionStatus = 'todo'):
        """
        Initialize a to-do list task item
        """

        self.description = description
        self.position = position
        self.completionStatus = completionStatus

    def __str__(self):
        """
        Return a human readable str representation of this task
        """

        return self.description