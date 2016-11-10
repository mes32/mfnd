#!/usr/bin/env python3
"""
MFND - A simple to-do list application
"""

import datetime
import sqlite3

def main():
    today = datetime.date.today()
    print( today.strftime("MFND - %B %d, %Y") )

if  __name__ =='__main__':
    main()
