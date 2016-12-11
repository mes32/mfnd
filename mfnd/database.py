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
        rowid INTEGER PRIMARY KEY,
        parentID INT DEFAULT NULL,
        description TEXT NOT NULL, 
        position INT NOT NULL,
        completionStatus TEXT NOT NULL DEFAULT 'todo', 
        visible INT, 
        mode_id INT
    );
    '''

    CREATE_TABLE_CLOSURETABLE = '''
    -- Closure Table of Tasks --
    CREATE TABLE IF NOT EXISTS ClosureTable (
        parentID INT NOT NULL, 
        childID INT NOT NULL,
        depth INT NOT NULL,
        FOREIGN KEY(parentID) REFERENCES TodoTask(rowid),
        FOREIGN KEY(childID) REFERENCES TodoTask(rowid)
    );
    '''

    CREATE_TRIGGER_TODOTASK_INSERT = '''
    -- Increment TodoTask.position before INSERT --
    CREATE TRIGGER IF NOT EXISTS TodoTask_insert AFTER INSERT ON TodoTask
    BEGIN
        UPDATE TodoTask SET parentID = new.rowid WHERE parentID IS NULL AND rowid = new.rowid;
        -- Insert into ClosureTable based on parentID
        -- Update should actually only order within a level
        UPDATE TodoTask SET position = position + 1 WHERE position >= new.position AND rowid != new.rowid;
    END;
    '''

    CREATE_TRIGGER_TODOTASK_DELETE = '''
    -- Decrement TodoTask.position after DELETE --
    CREATE TRIGGER IF NOT EXISTS TodoTask_delete AFTER DELETE ON TodoTask
    BEGIN
        UPDATE TodoTask SET position = position - 1 WHERE position > old.position;
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
        conn.isolation_level = None
        c = conn.cursor()

        # Create table TodoTask
        c.execute(self.CREATE_TABLE_TODOTASK)

        # Create table ClosureTable
        c.execute(self.CREATE_TABLE_CLOSURETABLE)

        # Create a trigger to increment TodoTask.position before INSERT
        c.execute(self.CREATE_TRIGGER_TODOTASK_INSERT)

        # Create a trigger to decrement TodoTask.position after DELETE
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
            c.execute("BEGIN")
            c.execute("DELETE FROM TodoTask;")
            c.execute("DELETE FROM ClosureTable;")
            c.execute("END")

        # Update the time of last initialization to current time 
        sql = '''
        UPDATE ConfigTime SET lastInitTime = \'''' + strSQLite(currentTime) + '''\' WHERE id = 1;
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

        sql = '''
        SELECT
            description,
            position,
            completionStatus
        FROM
            TodoTask
        ORDER BY
            position ASC;
        '''

        tasks = []
        for row in c.execute(sql):
            newTask = TodoTask(description = row[0], position = row[1], completionStatus = row[2])
            tasks.append(newTask)
        conn.commit()
        conn.close()

        return tasks

    def insertTask(self, task, position = None):
        """
        Insert a new task object into the database
        """

        conn = sqlite3.connect(self.databasePath)
        c = conn.cursor()

        if position == None:
            sql = '''
            INSERT INTO TodoTask (
                description,
                position
            ) VALUES (
                \'''' + strSQLite(task.description) + '''\',
                (SELECT COALESCE(MAX(position), 0) FROM TodoTask) + 1
            );
            '''
        else:
            sql = '''
            INSERT INTO TodoTask (
                description,
                position
            ) VALUES (
                \'''' + strSQLite(task.description) + '''\',
                ''' + strSQLite(position) + '''
            );
            '''  
        c.execute(sql)

        conn.commit()
        conn.close()

    def doneTask(self, position):
        """
        Update a task entry in the database
        """

        conn = sqlite3.connect(self.databasePath)
        c = conn.cursor()

        sql = '''
        UPDATE TodoTask
            SET completionStatus = 'done'
            WHERE position == ''' + strSQLite(position) + ''' ;
        '''
        c.execute(sql)

        conn.commit()
        conn.close()

    def deleteTask(self, position):
        """
        Update a task entry in the database
        """

        conn = sqlite3.connect(self.databasePath)
        c = conn.cursor()

        sql = '''
        DELETE FROM TodoTask
            WHERE position == ''' + strSQLite(position) + ''' ;
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
        UPDATE ConfigTime SET pumpkinTime = \'''' + strSQLite(timeInSecs) + '''\' WHERE id = 1;
        '''
        c.execute(sql)

        conn.commit()
        conn.close()

        print("New pumpkin time: " + timeInHours)
        print()

    def moveTask(self, currPosition, newPosition):
        """
        Move a task in the to-do list to a new position
        """

        task = self.getTask(currPosition)
        self.deleteTask(currPosition)
        self.insertTask(task, newPosition)

    def getTask(self, position):
        """
        Get a task from the to-do list based on it's position
        """

        conn = sqlite3.connect(self.databasePath)
        c = conn.cursor()

        sql = '''
        SELECT
            description,
            position,
            completionStatus
        FROM
            TodoTask
        WHERE
            position = ''' + strSQLite(position) + ''';
        '''

        for row in c.execute(sql):
            task = TodoTask(description = row[0], position = row[1], completionStatus = row[2])
            break
        conn.commit()
        conn.close()

        return task

    def moveUp(self, position):
        """
        Move a task up one position in the to-do list
        """

        self.moveTask(position, position - 1)

    def moveDown(self, position):
        """
        Move a task down one position in the to-do list
        """

        self.moveTask(position, position + 1)

    def moveTop(self, position):
        """
        Move a task to the top of the to-do list
        """

        self.moveTask(position, 1)

    def moveBottom(self, position):
        """
        Move a task to the bottom of the to-do list
        """

        self.moveTask(position, None)

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
