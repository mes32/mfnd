#!/usr/bin/env python3
"""
MFND - A simple to-do list application
"""

import datetime

def main():
    today = datetime.date.today()
    print( today.strftime("main MFND - %B %d, %Y") )

if  __name__ =='__main__':
    main()
