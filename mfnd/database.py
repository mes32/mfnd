#!/usr/bin/env python3
"""

Module for a database representing the to-do list

"""

import time
import sqlite3

from todotask import TodoTask
from tasktree import TaskTree
from tasktree import TreeNode

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

    class TaskIndexException(Exception):
        pass

    CREATE_TABLE_TODOTASK = '''
    -- Tasks to do --
    CREATE TABLE IF NOT EXISTS TodoTask (
        rowid INTEGER PRIMARY KEY,
        parentID INT DEFAULT NULL,
        description TEXT NOT NULL, 
        position INT NOT NULL,
        completionStatus TEXT NOT NULL DEFAULT 'todo'
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
        UPDATE TodoTask
            SET position = position + 1
            WHERE position >= new.position AND parentID = new.parentID AND rowid != new.rowid;

        INSERT INTO ClosureTable(
            parentID,
            childID,
            depth
        ) VALUES (
            new.rowid,
            new.rowid,
            0
        );

        INSERT INTO ClosureTable(
            parentID,
            childID,
            depth
        ) SELECT
            p.parentID,
            c.childID,
            p.depth + c.depth + 1
        FROM
            ClosureTable AS p,
            ClosureTable AS c
        WHERE p.childID = new.parentID AND c.parentID = new.rowid;
    END;
    '''

    CREATE_TRIGGER_TODOTASK_DELETE = '''
    -- Decrement TodoTask.position after DELETE --
    CREATE TRIGGER IF NOT EXISTS TodoTask_delete AFTER DELETE ON TodoTask
    BEGIN
        DELETE FROM ClosureTable
        WHERE childID IN (
            SELECT DISTINCT p.childID
            FROM ClosureTable p, ClosureTable c
            WHERE p.parentID = old.rowid AND c.childID = p.childID
        );

        DELETE FROM TodoTask 
        WHERE parentID = old.rowid;

        UPDATE TodoTask
            SET position = position - 1
            WHERE position > old.position AND parentID = old.parentID;
    END;
    '''

    INSERT_TODO_ROOT = '''
    INSERT INTO TodoTask (
        parentID,
        description, 
        position,
        completionStatus
    ) VALUES (
        NULL,
        '[root]',
        1,
        'na'
    );
    '''

    INSERT_TODO_DEFAULTMODE = '''
    INSERT OR IGNORE INTO TodoTask (
        parentID,
        description,
        position,
        completionStatus
    ) VALUES (
        1,
        '[default]',
        1,
        'na'
    );
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

            # Add initial entries into TodoTask
            c.execute(self.INSERT_TODO_ROOT)
            c.execute(self.INSERT_TODO_DEFAULTMODE)

        # Update the time of last initialization to current time 
        sql = '''
        UPDATE ConfigTime SET lastInitTime = \'''' + strSQLite(currentTime) + '''\' WHERE id = 1;
        '''
        c.execute(sql)

        conn.commit()
        conn.close()

    def initializeTaskTree(self, taskTree):
        """
        Initialize the task tree from the database
        """

        conn = sqlite3.connect(self.databasePath)
        c = conn.cursor()

        sql = '''
        SELECT 
            rowid,
            parentID,
            description,
            position,
            completionStatus,
            maxDepth
        FROM
            TodoTask AS t
        LEFT JOIN (
            SELECT
                childID,
                MAX(depth) AS maxDepth
            FROM
                ClosureTable
            GROUP BY childID
        )
        ON
            rowid = childID
        ORDER BY
            maxDepth ASC, position ASC;
        '''

        for row in c.execute(sql):
            rowid = row[0]
            parentID = row[1]
            description = row[2]
            position = row[3]
            completionStatus = row[4]
            maxDepth = row[5]

            task = TodoTask(description, position, completionStatus)
            node = TreeNode(rowid, parentID, task, maxDepth)
            taskTree.insertNode(node)

        conn.commit()
        conn.close()

    def insertTask(self, task, parentID):
        """
        Insert a new task object into the database
        """

        ########
        if task.position == None:
            print("insertTask() position = None")
        else:
            print("insertTask() position = " + str(task.position))
        ########

        if task.position == None:
            positionSQL = '(SELECT COALESCE(MAX(position), 0) FROM TodoTask WHERE parentID = ' + strSQLite(parentID) + ') + 1'
        else:
            positionSQL = strSQLite(task.position)

        conn = sqlite3.connect(self.databasePath)
        c = conn.cursor()

        sql = '''
        INSERT INTO TodoTask (
            parentID,
            description,
            position,
            completionStatus
        ) VALUES (
            ''' + strSQLite(parentID) + ''',
            \'''' + strSQLite(task.description) + '''\',
            ''' + strSQLite(positionSQL) + ''',
            \'''' + strSQLite(task.completionStatus) + '''\'
        );
        '''
        c.execute(sql)

        sql = '''
        SELECT last_insert_rowid() FROM TodoTask;
        '''
        rowid = 0
        for row in c.execute(sql):
            rowid = row[0]
            break

        sql = '''
        SELECT position FROM TodoTask WHERE rowid = ''' + strSQLite(rowid) + ''';
        '''
        for row in c.execute(sql):
            task.position = row[0]
            break

        conn.commit()
        conn.close()

        return rowid

    # def insertTree(self, tree):
    #     """
    #     Insert a tree of task objects into the database
    #     """

    #     self.insertTreeNode(tree.root, tree.position, tree.parentID)

    # def insertTreeNode(self, node, position, parentID):
    #     """
    #     Insert a tree node into the database
    #     """

    #     rowid = self.insertTask(node.task, position, None, parentID)
    #     childNodes = node.children

    #     index = 1
    #     for child in childNodes:
    #         self.insertTreeNode(child, index, rowid)
    #         index += 1

    def updateCompletionStatus(self, rowid, completionStatus):
        """
        Update 'completionStatus' for the task entry in the database under 'rowid'
        """

        conn = sqlite3.connect(self.databasePath)
        c = conn.cursor()

        sql = '''
        UPDATE TodoTask
            SET completionStatus = \'''' + completionStatus + '''\'
            WHERE rowid == ''' + strSQLite(rowid) + ''' ;
        '''
        c.execute(sql)

        conn.commit()
        conn.close()

        return rowid

    def deleteTask(self, rowid):
        """
        Delete a task entry from the database
        """

        conn = sqlite3.connect(self.databasePath)
        c = conn.cursor()

        sql = '''
        DELETE FROM TodoTask
            WHERE rowid == ''' + strSQLite(rowid) + ''' ;
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
