#!/usr/bin/env python3
"""

Module defining command tokens (Command Pattern) for use by the TodoShell CLI

"""


class Cmdtoken:
    """
    Abstract command class
    """

    def execute(self):
        """
        Execute this command
        """

    def undo(self):
        """
        Undo this command
        """
