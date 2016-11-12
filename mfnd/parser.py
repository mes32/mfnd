#!/usr/bin/env python3
"""

Module for parsing typed input commands

"""


class CommandParser:
    """
    Parse commands typed by the user to modify the to-do list
    """

    done = False

    def __init__(self, line):
        """
        Parse a line and set values accordingly
        """

        tokens = line.split()

        self.done = False
        if (tokens[0].lower() == "exit"):
            self.done = True

