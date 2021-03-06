#!/usr/bin/python

import glob
import os
import sys
import subprocess

'''Script that is used to access the map-folder of
hector_slam and copy its newest map-file (as png). 
Afterwards deletes all files in map-folder.

To be able to execute the command "convert" the package
imagemagick has to be installed.

The script has to be called with parameters.

:param 1: Path to hector_slam/hector_geotiff/maps.
:param 2: Path to folder where map will be copied to.
:param 3: New filename of copied map.
'''


SOURCE_FOLDER_PATH = sys.argv[1]
DESTINATION_FOLDER_PATH = sys.argv[2]
DESTINATION_FILE_NAME = sys.argv[3] + '.png'

def copy_last_geotiff_as_png():
    '''Copies newest geotiff file from SOURCE_FOLDER_PATH to 
    DESTINATION_FOLDER_PATH with DESTINATION_FILE_NAME as new
    filename and converted to png.
    '''
    source_file = get_newest_file_name('*.tif')
    subprocess.call(['convert', source_file, DESTINATION_FOLDER_PATH + DESTINATION_FILE_NAME])


def get_newest_file_name(searchpattern):
    '''Returns absolute path of newest .tif file in SOURCE_FOLDER_PATH.

    :param searchpattern: Searchpattern to look for.
    :returns: Absolute path of newest file that matches the searchpattern.
    '''
    files = filter(os.path.isfile, glob.glob(SOURCE_FOLDER_PATH + searchpattern))
    files.sort(key=lambda x: os.path.getmtime(x))
    return files[-1]


def copy_last_victim_csv():
    '''Copies last victim-csv file from SOURCE_FOLDER_PATH.'''
    source_file = get_newest_file_name('*_victims.csv')
    subprocess.call(['cp', source_file, DESTINATION_FOLDER_PATH + sys.argv[3] + '.csv'])


def clear_source_directory():
    '''Removes all files from SOURCE_FOLDER_PATH.'''
    files = glob.glob(SOURCE_FOLDER_PATH + '*')
    for f in files:
        os.remove(f)


copy_last_geotiff_as_png()
copy_last_victim_csv()
clear_source_directory()
