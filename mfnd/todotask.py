#!/usr/bin/env python3
"""

Module for tasks in the to-do list

"""


class TodoTask:
    """
    Represents a task in the to-do list
    """

    def __init__(self, description):
        """
        Initialize a to-do list task item
        """

        self.description = description
        self.completionStatus = 0
        self.visible = True
        self.mode = 0