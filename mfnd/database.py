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

        # Create table TodoTask
        sql = '''
        CREATE TABLE IF NOT EXISTS TodoTask (
            description TEXT NOT NULL, 
            taskOrder INT NOT NULL,
            completionStatus INT NOT NULL DEFAULT 0, 
            visible INT, 
            mode_id INT
        );
        '''
        c.execute(sql)

        # Create a trigger to increment TodoTask.taskOrder before INSERT
        sql = '''
        CREATE TRIGGER IF NOT EXISTS TodoTask_insert BEFORE INSERT ON TodoTask
        BEGIN
            UPDATE TodoTask SET taskOrder = taskOrder + 1 WHERE taskOrder >= new.taskOrder;
        END;
        '''
        c.execute(sql)

        # Create a trigger to decrement TodoTask.taskOrder after DELETE
        sql = '''
        CREATE TRIGGER IF NOT EXISTS TodoTask_delete AFTER DELETE ON TodoTask
        BEGIN
            UPDATE TodoTask SET taskOrder = taskOrder - 1 WHERE taskOrder > old.taskOrder;
        END;
        '''
        c.execute(sql)

        conn.commit()
        conn.close()

        # Insert four sample rows
        task = TodoTask("Put cover sheet on TPS report", 1)
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
        sql = '''
        SELECT
            description,
            taskOrder,
            completionStatus
        FROM
            TodoTask
        ORDER BY
            taskOrder ASC;
        '''

        tasks = []
        for row in c.execute(sql):
            newTask = TodoTask(row[0], row[1], row[2])
            tasks.append(newTask)
        conn.commit()
        conn.close()

        return tasks

    def insertTask(self, task):
        """
        Insert a new task object into the database
        """

        conn = sqlite3.connect(self.databasePath)
        c = conn.cursor()

        if task.taskOrder == -1:
            sql = '''
            INSERT INTO TodoTask (
                description,
                taskOrder
            ) VALUES (
                \'''' + str(task.description) + '''\',
                (SELECT MAX(taskOrder) FROM TodoTask) + 1
            );
            '''
        else:
            sql = '''
            INSERT INTO TodoTask (
                description,
                taskOrder
            ) VALUES (
                \'''' + str(task.description) + '''\',
                ''' + str(task.taskOrder) + '''
            );
            '''  
        c.execute(sql)

        conn.commit()
        conn.close()

    def doneTask(self, donePosition):
        """
        Update a task entry in the database
        """

        conn = sqlite3.connect(self.databasePath)
        c = conn.cursor()

        sql = '''
        UPDATE TodoTask
            SET completionStatus = 1 
            WHERE taskOrder == ''' + donePosition + ''' ;
        '''
        c.execute(sql)

        conn.commit()
        conn.close()

    def deleteTask(self, removePosition):
        """
        Update a task entry in the database
        """

        conn = sqlite3.connect(self.databasePath)
        c = conn.cursor()

        sql = '''
        DELETE FROM TodoTask
            WHERE taskOrder == ''' + removePosition + ''' ;
        '''
        c.execute(sql)

        conn.commit()
        conn.close()
