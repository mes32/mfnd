#!/usr/bin/env python3
"""

Module for input commands

"""

class CommandType():
    EXIT   = 1
    HELP   = 2
    TODO   = 3
    REMOVE = 4
    DONE   = 5

class CommandParser:
    """
    Parse commands typed by the user to modify the to-do list
    """

    def __init__(self, line):
        """
        Parse a line and set values accordingly
        """

        tokens = line.split()

        if (tokens[0].lower() == "exit"):
            self.type = CommandType.EXIT
            return
        elif (tokens[0].lower() == "help"):
            self.type = CommandType.HELP
            return

