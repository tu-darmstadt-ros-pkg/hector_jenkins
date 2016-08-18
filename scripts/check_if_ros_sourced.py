#!/usr/bin/python
import os
import sys

'''Script that tests if a ROS environment is sourced.
If so, the script terminates with an exitcode of 1.
'''

exists = False

try:
    result =  os.environ['ROS_DISTRO']
    exists = True
except KeyError:
    pass

if exists:
    print 'Error: A ROS environment seems to be sourced.'
    sys.exit([1])
else:
    print 'No ROS environment seems to be sourced.'
    sys.exit()
