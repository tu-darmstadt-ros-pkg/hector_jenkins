#!/usr/bin/python

import sys
import subprocess
import os


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

installation_folder_path = '/home/hector/stefan-testing/hector_tracker_install'
print(sys.stdout.encoding)

with cd(installation_folder_path):
    result = subprocess.check_output('./update.sh')
    if '[build] Failed: No packages failed.' not in result:
        sys.exit([1])

    optional_requirements = ['gazebo_sim.rosinstall', 'gui.rosinstall', 
                             'integration_testing.rosinstall', 'icp_mapping.rosinstall']
    for optional_requirement in optional_requirements:
        commandList = ('wstool merge optional_installs/' + optional_requirement).split(' ')
        print subprocess.check_output(commandList)

    print subprocess.check_output(['wstool', 'update'])
    result = subprocess.check_output(['catkin', 'build'])
    if '[build] Failed: No packages failed.' not in result:
        sys.exit([1])
