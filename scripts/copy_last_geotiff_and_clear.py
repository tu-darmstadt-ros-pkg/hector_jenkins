#!/usr/bin/python

import glob
import os
import shutil
import sys

'''Script that is used to access the map-folder of
hector_slam and copy its newest map-file. Afterwards
deletes all files in map-folder.

The script has to be called with parameters.

:param 1: Path to hector_slam/hector_geotiff/maps.
:param 2: Path to folder where map will be copied to.
:param 3: New filename of copied map.
'''


SOURCE_FOLDER_PATH = sys.argv[1]
DESTINATION_FOLDER_PATH = sys.argv[2]
DESTINATION_FILE_NAME = sys.argv[3]

def copy_last_geotiff():
    '''Copies newest geotiff file from SOURCE_FOLDER_PATH to 
    DESTINATION_FOLDER_PATH with DESTINATION_FILE_NAME as new
    filename.
    '''
    source_file = get_newest_file_name()
    shutil.copy(source_file, DESTINATION_FOLDER_PATH + DESTINATION_FILE_NAME + '.tif')

def get_newest_file_name():
    '''Returns absolute path of newest .tif file in SOURCE_FOLDER_PATH.'''
    files = filter(os.path.isfile, glob.glob(SOURCE_FOLDER_PATH + "*.tif"))
    files.sort(key=lambda x: os.path.getmtime(x))
    return files[-1]

def clear_source_directory():
    '''Removes all files from SOURCE_FOLDER_PATH.'''
    files = glob.glob(SOURCE_FOLDER_PATH + '*')
    for f in files:
        os.remove(f)


copy_last_geotiff()
clear_source_directory()