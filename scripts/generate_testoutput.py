#!/usr/bin/python

from junit_xml import TestSuite, TestCase
import glob
import statistics
import getpass
import os
import sys


'''This script generates testoutputs that will be used by the HTMLPublisher
plugin to display results of the build.

This script needs junit-xml and statistics to be installed via pip.
The script has one parameter that defines the number of files
that will be looked for.
'''

USERNAME = getpass.getuser()
CURDIR = os.path.dirname(__file__)
NUM_FILES = int(sys.argv[1])


def process_victim_files():
    '''Reads last NUM_FILES victim files from exploration run
    and returns final number of found victims as a list.
    '''
    victim_files = glob.glob(os.path.join(CURDIR, 'scriptoutputs/html/*.csv'))
    victim_files.sort()
    victim_files = victim_files[-NUM_FILES:]
    victim_counts = []
    for victim_file in victim_files:
        currently_open_file = open(victim_file, 'r')
        #first 6 lines contain only file information.
        lines = currently_open_file.readlines()[6:]
        victim_counts.append(len(lines))
        currently_open_file.close()
        
    return victim_counts


def create_junit_file(victim_count):
    '''Creates a JUnit-xml file that contains a number of
    test cases equal to victim_count.
    '''
    test_cases = []
    i = 0
    while i < victim_count:
        test_cases.append(TestCase('Test' + str(i), 'some.class.name', 123.345, 'I am stdout!', 'I am stderr!'))
        i = i +1

    ts = TestSuite("my test suite", test_cases)
    with open(os.path.join(CURDIR, 'scriptoutputs/junit/output.xml'), 'w') as f:
        TestSuite.to_file(f, [ts], prettyprint=False)


def create_html_file(victim_counts):
    '''Creates a HTML file that contains a table displaying
    the map exploration and victim found results for all runs.
    '''
    file_to_write = open(os.path.join(CURDIR, 'scriptoutputs/html/last_run.html'), 'w')
    file_to_write.write('<h1>Exploration Evaluation Results</h1>')
    file_to_write.write('<table border="1">')
    file_to_write.write('<tr>')
    file_to_write.write(('<th>Trial Number </th><th>Victims Found</th>'
                         + '<th>Map</th><th>Logfiles</th>'))
    file_to_write.write('</tr>')
    i = 0
    while i < len(victim_counts):
        file_to_write.write('<tr>')
        file_to_write.write('<td>' + str(i+1) + '</td><td>' + str(victim_counts[i]) +
                            '</td>')
        file_to_write.write('<td><img src="'+ str(i+1) +'.png"></td>')
        file_to_write.write('<td><a href="'+ str(i+1) +'.zip">Log</a></td>')
        file_to_write.write('</tr>')
        i = i + 1

    file_to_write.write('</table>')
    file_to_write.close()


victim_counts = process_victim_files()

create_junit_file(statistics.median(victim_counts))
create_html_file(victim_counts)

