##
# @file codebase_test_data_tracker.py
#
# @copyright Copyright (C) 2013-2014 srcML, LLC. (www.srcML.org)
# 
# The stereocode is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# The stereocode Toolkit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with the stereocode Toolkit; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys, stereocode, srcml, lxml.etree as et, lxml, os
from xslt_util import *
# from lxml.etree import XMLParser, parse
# p = XMLParser(huge_tree=True)
# tree = parse('file.xml', parser=p)


class StereotypeDocData:
    def __init__(self):
        self.filename = ""
        self.directory = ""
        self.outputFolderName = ""
        self.initialHistogram = dict()
        self.currentHistogram = dict()
        self.processedFunctionCount = 0
        self.mismatchedFunctionStereotype = []

DataFolderName = "stereocode"

class CodeBaseTestDataTracker:
    def __init__(self):
        self.testData = []
        self.data = None

    def runTest(self, testFile):
        if os.stat(testFile).st_size == 0:
            os.remove(testFile)
            return
        self.data = StereotypeDocData()
        self.data.filename = testFile
        self.data.directory =  os.path.dirname(testFile)
        self.data.outputFolderName = os.path.join(self.data.directory, os.path.split(testFile)[0] + DataFolderName)
        self.testData.append(self.data)
        p = et.XMLParser(huge_tree = True)

        print 80 * "~"
        print "Processing Document: {0}: {1}".format(len(self.testData), testFile) 
        print 80 * "~"
        print self.data.outputFolderName

        # Loading current document for processing
        initialDocument = et.parse(testFile, parser=p)
        generateStereotypeReportFromDoc(initialDocument)


    def OutputTestData(self):
        raise NotImplementedError()


    # def printOutputData(self):
    #     raise NotImplementedError()