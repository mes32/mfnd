#!/usr/bin/env python3
"""

Module for a database representing the to-do list

"""

import sqlite3

class TodoDatabase:
    """
    Represents an SQLite database storing tasks in a to-do list
    """

    databasePath = ""

    def __init__(self, databasePath):
        """
        Initialize the database
        """

        self.databasePath = databasePath
        conn = sqlite3.connect(databasePath)
        c = conn.cursor()

        # Create table
        sql = '''CREATE TABLE IF NOT EXISTS TodoTask (
                     description TEXT NOT NULL, 
                     completionStatus INT NOT NULL, 
                     visible INT, 
                     mode_id INT
                 );'''
        c.execute(sql)

        # Insert some sample rows
        sql = '''INSERT INTO TodoTask (
                     description,
                     completionStatus
                 ) VALUES (
                     'Put cover sheet on TPS report',
                     0
                 );'''
        c.execute(sql)
        sql = '''INSERT INTO TodoTask (
                     description,
                     completionStatus
                 ) VALUES (
                     'Put cover sheet on TPS report',
                     0
                 );'''
        c.execute(sql)
        sql = '''INSERT INTO TodoTask (
                     description,
                     completionStatus
                 ) VALUES (
                     'Put cover sheet on TPS report',
                     0
                 );'''
        c.execute(sql)


        conn.commit()
        conn.close()

    def getTasks(self):
        """
        Return a list of all tasks stored in the database
        """

        conn = sqlite3.connect(self.databasePath)
        c = conn.cursor()

        # Create table
        sql = '''SELECT description FROM TodoTask WHERE completionStatus = 0;'''

        tasks = []
        for row in c.execute(sql):
            tasks.append(row[0])
        conn.commit()
        conn.close()

        return tasks