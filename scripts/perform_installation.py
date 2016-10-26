#!/usr/bin/python
import sys
import subprocess
import os

'''The script has to be called with the path to the hector_tracker_install folder
that should be used.
'''

HECTOR_TRACKER_INSTALL_PATH = sys.argv[1]

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

with cd(HECTOR_TRACKER_INSTALL_PATH):
    result = subprocess.check_output('./update.sh')
    print("Output of ./update.sh: \n" + result)
    if '[build] Failed: No packages failed.' not in result:
        sys.exit([1])

    optional_requirements = ['gazebo_sim.rosinstall', 'gui.rosinstall', 
                             'integration_testing.rosinstall', 'icp_mapping.rosinstall']
    for optional_requirement in optional_requirements:
        commandList = ('wstool merge optional_installs/' + optional_requirement).split(' ')
        result = subprocess.check_output(commandList)
        print("Output of wstool merge:\n" + result )

    result = subprocess.check_output(['wstool', 'update'])
    print("Output of wstool update: \n" + result)
    result = subprocess.check_output(['catkin', 'build'])
    print("Output of catkin build: \n" + result)
    if '[build] Failed: No packages failed.' not in result:
        sys.exit([1])


