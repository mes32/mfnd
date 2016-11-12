#!/usr/bin/env python3
"""

Module for a database representing the to-do list

"""

import sqlite3
from todotask import TodoTask

class TodoDatabase:
    """
    Represents an SQLite database storing tasks in a to-do list
    """

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

        conn.commit()
        conn.close()

        # Insert four sample rows
        task = TodoTask("Put cover sheet on TPS report")
        self.insertTask(task)
        self.insertTask(task)
        self.insertTask(task)
        self.insertTask(task)

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
            tasks.append(TodoTask(row[0]))
        conn.commit()
        conn.close()

        return tasks

    def insertTask(self, task):
        """
        Insert a new task object into the database
        """

        conn = sqlite3.connect(self.databasePath)
        c = conn.cursor()

        sql = '''INSERT INTO TodoTask (
                     description,
                     completionStatus
                 ) VALUES (
                     \'''' + task.description + '''\',
                     ''' + str(task.completionStatus) + '''
                 );'''
        c.execute(sql)

        conn.commit()
        conn.close()