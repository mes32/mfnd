#!/usr/bin/env python3
"""

Module for a database representing the to-do list

"""

import time
import sqlite3

from todotask import TodoTask

def strSQLite(string):
    """
    Sanitizes input for SQLite TEXT fields by converting to string and replacing 
    each single quote (') with two single quotes ('')
    """

    return str(string).replace(r"'", "''")

class TodoDatabase:
    """
    Represents an SQLite database storing tasks in a to-do list
    """

    CREATE_TABLE_TODOTASK = '''
    -- Tasks to do --
    CREATE TABLE IF NOT EXISTS TodoTask (
        description TEXT NOT NULL, 
        taskOrder INT NOT NULL,
        completionStatus INT NOT NULL DEFAULT 0, 
        visible INT, 
        mode_id INT
    );
    '''

    CREATE_TRIGGER_TODOTASK_INSERT = '''
    -- Increment TodoTask.taskOrder before INSERT --
    CREATE TRIGGER IF NOT EXISTS TodoTask_insert BEFORE INSERT ON TodoTask
    BEGIN
        UPDATE TodoTask SET taskOrder = taskOrder + 1 WHERE taskOrder >= new.taskOrder;
    END;
    '''

    CREATE_TRIGGER_TODOTASK_DELETE = '''
    -- Decrement TodoTask.taskOrder after DELETE --
    CREATE TRIGGER IF NOT EXISTS TodoTask_delete AFTER DELETE ON TodoTask
    BEGIN
        UPDATE TodoTask SET taskOrder = taskOrder - 1 WHERE taskOrder > old.taskOrder;
    END;
    '''

    CREATE_TABLE_CONFIGTIME = '''
    CREATE TABLE IF NOT EXISTS ConfigTime (
        id INTEGER PRIMARY KEY,
        pumpkinTime INT NOT NULL,
        lastInitTime INT DEFAULT 0
    );
    '''

    SETUP_CONFIGTIME = '''
    INSERT OR IGNORE INTO ConfigTime (
        id,
        pumpkinTime
    ) VALUES (
        1,
        '14400'
    );
    '''


    def __init__(self, databasePath):
        """
        Initialize the database
        """

        self.databasePath = databasePath
        conn = sqlite3.connect(databasePath)
        c = conn.cursor()

        # Create table TodoTask
        c.execute(self.CREATE_TABLE_TODOTASK)

        # Create a trigger to increment TodoTask.taskOrder before INSERT
        c.execute(self.CREATE_TRIGGER_TODOTASK_INSERT)

        # Create a trigger to decrement TodoTask.taskOrder after DELETE
        c.execute(self.CREATE_TRIGGER_TODOTASK_DELETE)

        # Create table ConfigTime
        # Set the default pumpkinTime, but allow the possibility it was previously configured
        c.execute(self.CREATE_TABLE_CONFIGTIME)
        c.execute(self.SETUP_CONFIGTIME)

        sql = '''
        SELECT pumpkinTime FROM ConfigTime WHERE id = 1;
        '''
        result = c.execute(sql)
        result_list = result.fetchall()  
        pumpkinTime = int(result_list[0][0])

        sql = '''
        SELECT lastInitTime FROM ConfigTime WHERE id = 1;
        '''
        result = c.execute(sql)
        result_list = result.fetchall()  
        lastInitTime = int(result_list[0][0])

        # Find the time of the most recent reset point based on the current time
        (lastPumpkinTime, currentTime) = self.__getLastPumpkinTime(pumpkinTime)

        # Compute durations since last reset and since last database initialization
        sincePumpkin = int(currentTime) - int(lastPumpkinTime)
        sinceInit = int(currentTime) - int(lastInitTime)

        # If a reset point 'pumpkin time' is more recent than the last database initialization, 
        # it's a new day therefore delete the entire TodoTask table
        if sincePumpkin < sinceInit:
            sql = '''
            DELETE FROM TodoTask;
            '''
            c.execute(sql)

        # Update the time of last initialization to current time 
        sql = '''
        UPDATE ConfigTime SET lastInitTime = \'''' + str(currentTime) + '''\' WHERE id = 1;
        '''
        c.execute(sql)

        conn.commit()
        conn.close()

        # Insert four sample rows
        task = TodoTask("Put cover sheet on TPS report (A)")
        self.insertTask(task)
        task = TodoTask("Put cover sheet on TPS report (B)")
        self.insertTask(task)
        task = TodoTask("Put cover sheet on TPS report (C)")
        self.insertTask(task)
        task = TodoTask("Put cover sheet on TPS report (D)")
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

    def insertTask(self, task, num = None):
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
                \'''' + strSQLite(task.description) + '''\',
                (SELECT COALESCE(MAX(taskOrder), 0) FROM TodoTask) + 1
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
            WHERE taskOrder == ''' + str(donePosition) + ''' ;
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
            WHERE taskOrder == ''' + str(removePosition) + ''' ;
        '''
        c.execute(sql)

        conn.commit()
        conn.close()

    def configurePumpkinTime(self, timeInHours):
        """
        Configure the time of day at which the TodoTask table resets
        """

        hours = int(timeInHours[:2]) % 24
        mins = int(timeInHours[2:]) % 60
        timeInSecs = 60*60*hours + 60*mins

        conn = sqlite3.connect(self.databasePath)
        c = conn.cursor()

        sql = '''
        UPDATE ConfigTime SET pumpkinTime = \'''' + str(timeInSecs) + '''\' WHERE id = 1;
        '''
        c.execute(sql)

        conn.commit()
        conn.close()

        print("New pumpkin time: " + timeInHours)
        print()

    def __moveTask(self, currentNum, newNum):
        task = self.__getTask(currentNum)
        self.__deleteTask(currentNum)
        self.insertTask(task, newNum)

    def __getTask(self, num):
        return num

    def __deleteTask(self, num):
        return num

    def moveUp(self, num):
        """
        Move a task up one position in the to-do list
        """

        taskList = self.getTasks()
        task = taskList[num - 1]
        self.deleteTask(num)
        task.taskOrder = num - 1
        self.insertTask(task)

    def moveDown(self, num):
        """
        Move a task down one position in the to-do list
        """

        taskList = self.getTasks()
        task = taskList[num - 1]
        self.deleteTask(num)
        task.taskOrder = num + 1
        self.insertTask(task)


    def __getLastPumpkinTime(self, pumpkinTime):
        """
        Return the time of the most recent reset point (pumpkin time) and the current time it is relative to
        """
        lt = time.localtime()
        currentTime = time.mktime(lt)

        # Relative to the current time find the most recent pumpkin time (lastPumpkinTime)
        # Based on pumpkin time as time-of-day (pumpkinTime)
        lt = time.localtime(currentTime - pumpkinTime)
        hours = lt.tm_hour
        mins = lt.tm_min
        secs = lt.tm_sec
        secsBack = 60*60*hours + 60*mins + secs
        lastPumpkinTime = currentTime - secsBack

        return (int(lastPumpkinTime), int(currentTime))
