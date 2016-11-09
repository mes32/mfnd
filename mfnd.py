#!/usr/bin/env python3
"""
MFND - A simple to-do list application
"""

import datetime

today = datetime.date.today()

print( today.strftime('MFND - %B %d, %Y') )
