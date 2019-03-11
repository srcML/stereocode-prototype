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

def cleanFile(fileName):
	file = open(fileName)
	contents = file.read().strip()
	file.close()

	return contents.splitlines()

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
		diff = list(difflib.unified_diff(cleanFile('suite/' + file), cleanFile(basename + '_transformed.xml'), lineterm=''))

		# count success and failure and not crash or quit on failure
		if len(diff) > 0:
			print basename + '_transformed.xml'
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

current_dir = os.getcwd()
for eachFile in os.listdir(current_dir):
	if os.path.splitext(eachFile)[1] == '.cpp' or os.path.splitext(eachFile)[1] == '.xml':		
		try:
			os.remove(eachFile)
		except Exception as e:
			print(e)
	else:
		continue

# print how many passed and failed.
if error_count == 0:
    print "Errors: 0 out of " + str(total_count) + " cases"
else:
	print "Passed tests:  " + str(passed_count) + " out of " + str(total_count) + " cases"
	print "Errors found:  " + str(error_count) + " out of " + str(total_count) + " cases"


exit
