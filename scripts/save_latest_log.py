#!/usr/bin/python
import sys
import subprocess
import getpass

USERNAME = getpass.getuser()
LOG_FOLDER_PATH = '/home/' + USERNAME + '/.ros/log/latest'
DESTINATION_FOLDER_PATH = sys.argv[1]
DESTINATION_FILE_NAME = sys.argv[2] + '.zip'

subprocess.call(['zip', '-r', DESTINATION_FOLDER_PATH + DESTINATION_FILE_NAME, LOG_FOLDER_PATH])
