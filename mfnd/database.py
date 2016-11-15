#!/usr/bin/env python3
"""

Module for a database representing the to-do list

"""

import time
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

        # Create table ConfigTime
        sql = '''
        CREATE TABLE IF NOT EXISTS ConfigTime (
            id INTEGER PRIMARY KEY,
            pumpkinTime INT NOT NULL,
            lastInitTime INT DEFAULT 0
        );
        '''
        c.execute(sql)

        sql = '''
        INSERT OR IGNORE INTO ConfigTime (
            id,
            pumpkinTime
        ) VALUES (
            1,
            '14400'
        );
        '''
        c.execute(sql)

        sql = '''
        SELECT pumpkinTime FROM ConfigTime WHERE id = 1;
        '''
        result = c.execute(sql)
        result_list = result.fetchall()  
        pumpkinTime = int(result_list[0][0])
        print("pumpkinTime = " + str(pumpkinTime))

        sql = '''
        SELECT lastInitTime FROM ConfigTime WHERE id = 1;
        '''
        result = c.execute(sql)
        result_list = result.fetchall()  
        lastInitTime = int(result_list[0][0])

        # if lastInitTime == None:
        #     lastInitTime = 0
        #     print("lastInitTime = " + str(lastInitTime))
        # else:
        #     lastInitTime = int(lastInitTime)
        #     print("lastInitTime = " + str(lastInitTime))
        (lastPumpkinTime, currentTime) = self.__getLastPumpkinTime(pumpkinTime)
        #(lastPumpkinTime, currentTime) = self.__getLastPumpkinTime(14400)

        sincePumpkin = int(currentTime) - int(lastPumpkinTime)
        sinceInit = int(currentTime) - int(lastInitTime)

        # print()
        # print("currentTime = " + str(int(currentTime)))
        # print("lastPumpkinTime = " + str(int(lastPumpkinTime)))
        # print("lastInitTime = " + str(int(lastInitTime)))
        # print("")
        # print("sincePumpkin = " + str(int(sincePumpkin)))
        # print("sinceInit = " + str(int(sinceInit)))

        if sincePumpkin < sinceInit:
            # print("*** DELETE FROM TodoTask ***")
            sql = '''
            DELETE FROM TodoTask;
            '''
            c.execute(sql)

        sql = '''
        UPDATE ConfigTime SET lastInitTime = \'''' + str(currentTime) + '''\' WHERE id = 1;
        '''
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

    def __getLastPumpkinTime(self, pumpkinTime):
        lt = time.localtime()
        currentTime = time.mktime(lt)

        lt = time.localtime(currentTime - pumpkinTime)
        hours = lt.tm_hour
        mins = lt.tm_min
        secs = lt.tm_sec
        offSetTime = 60*60*hours + 60*mins + secs
        lastPumpkinTime = currentTime - offSetTime

        return (int(lastPumpkinTime), int(currentTime))