#!/usr/bin/python

import os
from subprocess import check_output
import difflib


# total number of errors
error_count = 0

# total test cases
total_count = 0

# total number of passed tests
passed_count = 0

try:

	# file both input and answer
	for file in os.listdir('suite') :
		#check for files with .cpp extension
		if os.path.splitext(file)[1] != ".xml":
			continue

		basename = os.path.splitext(file)[0]

		# generate source
		check_output(['srcml', 'suite/' + file, '-o', basename])

		# regenerate xml without answer
		check_output(['srcml', basename, '-o', basename + '_input.xml'])

		# run test
		check_output(['python', 'stereocode.py', '-m', 'XmlAttr', '-i', basename + '_input.xml', '-o', basename + '_transformed.xml'])

		# verify test
		diff = difflib.unified_diff(open('suite/' + file).readlines(), open(basename + '_transformed.xml').readlines(), lineterm='')

		# count success and failure and not crash or quit on failure
		if len(list(diff)) > 0:
			error_count = error_count + 1
		else:
			passed_count = passed_count + 1

		total_count = total_count + 1

	ki = False
except KeyboardInterrupt:
    ki = True

print "Report:"
if ki:
    print "Testing stopped by keyboard"

# print how many passed and failed.
if error_count == 0:
    print "Errors: 0 out of " + str(total_count) + " cases"
else:
	print "Passed tests:  " + str(passed_count) + " out of " + str(total_count) + " cases"
	print "Errors found:  " + str(error_count) + " out of " + str(total_count) + " cases"


exit
