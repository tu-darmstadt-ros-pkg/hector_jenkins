#!/usr/bin/python

from junit_xml import TestSuite, TestCase
import glob
import statistics
import getpass
import os
import sys


'''... TODO.

This script needs junit-xml and statistics to be installed via pip.
The script has one parameter that defines the number of files
that will be looked for.
'''

USERNAME = getpass.getuser()
CURDIR = os.path.dirname(__file__)
NUM_FILES = int(sys.argv[1])

def process_map_files():
    '''Reads last 5 map result files from exploration run
    and returns final percentage of map discovery for each
    run a list.
    '''
    map_files = glob.glob('/home/' + USERNAME+ '/.ros/*_map_data.csv')
    map_files.sort()
    map_files = map_files[-NUM_FILES:]
    map_results = []
    for map_file in map_files:
        percentage_discovered = 0
        currently_open_file = open(map_file, 'r')
        lines = currently_open_file.readlines()
        if len(lines) != 0:
            percentage_discovered = lines[-1].split(',')[1]

        map_results.append(percentage_discovered)
        currently_open_file.close()

    return map_results


def process_victim_files():
    '''Reads last 5 victim files from exploration run
    and returns final number of found victims as a list.
    '''
    victim_files = glob.glob('/home/' + USERNAME + '/.ros/*_victim_data.csv')
    victim_files.sort()
    victim_files = victim_files[-5:]
    victim_counts = []
    for victim_file in victim_files:
        num_victims = 0
        currently_open_file = open(victim_file, 'r')
        lines = currently_open_file.readlines()
        if len(lines) != 0:
            num_victims = num_victims + 1

        currently_open_file.close()
        victim_counts.append(num_victims)

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


def create_html_file(map_results, victim_counts):
    '''Creates a HTML file that contains a table displaying
    the map exploration and victim found results for all runs.
    '''
    file_to_write = open(os.path.join(CURDIR, 'scriptoutputs/html/last_run.html'), 'w')
    file_to_write.write('<h1>Exploration Evaluation Results</h1>')
    file_to_write.write('<table border="1">')
    file_to_write.write('<tr>')
    file_to_write.write('<th>Trial Number </th><th>Victims Found</th><th>Final map discovery</th><th>Map</th>')
    file_to_write.write('</tr>')
    i = 0
    while i < len(map_results):
        file_to_write.write('<tr>')
        file_to_write.write('<td>' + str(i+1) + '</td><td>' + str(victim_counts[i]) +
                            '</td><td>' + str(map_results[i]) + '%</td>')
        file_to_write.write('<td><img src="'+ str(i+1) +'.png"></td>')
        file_to_write.write('</tr>')
        i = i + 1

    file_to_write.write('</table>')
    file_to_write.close()


map_results = process_map_files()
victim_counts = process_victim_files()

create_junit_file(statistics.median(victim_counts))
create_html_file(map_results, victim_counts)
