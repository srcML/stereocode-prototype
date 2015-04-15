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

import sys, stereocode, lxml.etree as et, lxml, os, os.path
from xslt_util import *
from srcml import *
class StereotypeDocData:
    def __init__(self):
        self.filename = ""
        self.directory = ""
        self.outputFolderName = ""
        self.initialHistogram = dict()
        self.currentHistogram = dict()
        self.initialStereotypeInfo = []
        self.currentStereotypeInfo = []
        # self.processedFunctionCount = 0
        # self.mismatchedFunctionStereotype = []
        self.testResultErrorText = []

DataFolderName = "archive_test_data/reports"


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
        self.testData.append(self.data)

        print 80 * "~"
        print "Processing Document: {0}: {1}".format(len(self.testData), testFile) 
        print 80 * "~"
        sys.stdout.flush()

        # Loading current document for processing
        print "  Loading Initial Document"
        sys.stdout.flush()
        p = et.XMLParser(huge_tree = True)
        oldStereotypedDocument = et.parse(testFile, parser=p)
        print "  Getting info from doc"
        sys.stdout.flush()
        oldStereotypedFunctionInfo = generateStereotypeReportFromDoc(oldStereotypedDocument)
        self.data.initialStereotypeInfo = oldStereotypedFunctionInfo
        self.data.initialHistogram = buildHistogram(oldStereotypedFunctionInfo)
        
        removePreviousStereotypeCommentXSLTDoc = """<?xml version="1.0" encoding="utf-8"?>
        <xsl:stylesheet version="1.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:src="http://www.sdml.info/srcML/src"
        xmlns:regexp="http://exslt.org/regular-expressions"
        >
 <xsl:output omit-xml-declaration="no"/>

    <xsl:template match="node()|@*">
      <xsl:copy>
         <xsl:apply-templates select="node()|@*"/>
      </xsl:copy>
    </xsl:template>

    <xsl:template match="//src:comment"/>
</xsl:stylesheet>
        """

        print "  Removing comments"
        sys.stdout.flush()
        removeStereotypesTransform = et.XSLT(et.XML(removePreviousStereotypeCommentXSLTDoc))
        tempInputBuffer = memory_buffer()
        print "  Loading doc w/o comments"
        sys.stdout.flush()
        tempInputBuffer.load_from_string(et.tostring(removeStereotypesTransform(oldStereotypedDocument)))
        del oldStereotypedDocument
        temp_buffer = memory_buffer()
        print "  Reprocessing with srcML"
        sys.stdout.flush()
        with readable_archive(readable_archive_settings(), buffer=tempInputBuffer) as reader:
            with writable_archive(writable_archive_settings(default_language=LANGUAGE_CXX), buffer=temp_buffer) as outputArch:
                currentUnit = reader.read()
                while currentUnit != None:
                    # print currentUnit.filename
                    outputUnit = outputArch.create_unit(filename=currentUnit.filename)
                    outputUnit.parse(source_code=currentUnit.unparse())
                    outputArch.write(outputUnit)
                    currentUnit = reader.read()
        print "  Reloading re-srcML-i-fied document"
        sys.stdout.flush()
        noCommentDoc = et.XML(temp_buffer.to_string())
        temp_buffer.free()
        del temp_buffer
        print "  Transforming re-srcmlified document with stereocode"
        sys.stdout.flush()
        redocumentedDoc = stereocode.stereocodeDoc(noCommentDoc)

        print "  Extracting new stereotype information from document"
        sys.stdout.flush()
        newStereotypeInfo = generateStereotypeReportFromDoc(redocumentedDoc)
        del redocumentedDoc
        self.data.currentStereotypeInfo = newStereotypeInfo
        self.data.currentHistogram = buildHistogram(newStereotypeInfo)

        print "  Analyzing Stereotype document"
        sys.stdout.flush()


        # Comparing Expected and actual to see if they
        # are the same or not.
        outputDocumentPathFilePrefix = os.path.split(testFile)[1]
        reportFilePath = os.path.join(DataFolderName, outputDocumentPathFilePrefix + ".testResults.txt")

        reportStrm = open(reportFilePath, "w")
        reportStrm.write("Function Counts\n  Expected: {0}\n Actual: {1}\n".format(len(self.data.initialStereotypeInfo), len(self.data.currentStereotypeInfo)))
        # if len(self.data.initialStereotypeInfo) != len(self.data.currentStereotypeInfo):
        #     self.data.testResultErrorText.append("Mismatched number of stereotyped functions.")

        reportStrm.write("Histogram Comparison\n")
        reportStrm.write("Total # of Unique stereotype Combinations: \n")
        reportStrm.write("  Expected: {0}\n  Actual: {1}\n".format(len(self.data.initialHistogram), len(self.data.currentHistogram)))
        initialHistogramList = sorted(self.data.initialHistogram.items(), key=lambda x: x[1])
        currentHistogramList = sorted(self.data.currentHistogram.items(), key=lambda x: x[1])

        hasHistogramError = False
        if len(self.data.initialHistogram) != len(self.data.currentHistogram):
            self.data.testResultErrorText.append("Mismatched number of unique stereotype combinations.")
            extraCategories = list(set([x[0] for x in initialHistogramList]) - set([x[0] for x in currentHistogramList]))
            reportStrm.write("Extra Categories: \n")
            reportStrm.write("\n".join(extraCategories) + "\n")
            self.data.testResultErrorText.append("Extra Categories: {0}".format("\n".join(extraCategories)))
            hasHistogramError = True
        else:
            histogramIndex = 0
            for histData in zip(initialHistogramList, currentHistogramList):
                if histData[0][0] != histData[1][0]:
                    hasHistogramError = True
                    errMsg = "Mismatched histogram ordering @Index: {2}:\n  Expected: {0}\n  Actual: {1}\n".format(histData[0][0],  histData[1][0], index)
                    reportStrm.write(errMsg)
                    self.data.testResultErrorText.append(errMsg)
                if histData[0][1] != histData[1][1]:
                    hasHistogramError = True
                    errMsg = "Mismatched histogram item count @Index: {4}:\n  Expected: {0}: {1}\n  Actual: {2}: {3}\n".format(
                        histData[0][0], histData[0][1],
                        histData[1][0], histData[1][1],
                        index
                    )
                    reportStrm.write(errMsg)
                    self.data.testResultErrorText.append(errMsg)
                histogramIndex += 1

        # Outputting Histogram in the event of an error.
        if hasHistogramError:
            reportStrm.write("Expected Histogram\n")
            for entry in initialHistogramList:
                reportStrm.write("  {1:>6}: {0}\n".format(*entry))
            reportStrm.write("\n\n")
            reportStrm.write("Actual Histogram\n")
            for entry in currentHistogramList:
                reportStrm.write("  {1:>6}: {0}\n".format(*entry))
            reportStrm.write("\n\n")
        else:
            reportStrm.write("Has Equivalent Histograms\n")

        # Checking Functions within the System.

        hasMissingFunctions = False
        if len(self.data.initialStereotypeInfo) != len(self.data.currentStereotypeInfo):
            self.data.testResultErrorText.append("Mismatched number of stereotyped functions.")
            hasMissingFunctions = True
            self.outputMissingFunctions(reportStrm)

        else:
            # Doing a set difference to see if the same functions exist within both
            # sets of function info.
            initialFunctionSigSet = set([x[0] for x in self.data.initialStereotypeInfo])
            currentFunctionSigSet = set([x[0] for x in self.data.currentStereotypeInfo])

            if len(initialFunctionSigSet) != len(self.data.initialStereotypeInfo):
                raise Exception("Error not all function signatures are unique within initial document. Alter naming convention!")

            if len(currentFunctionSigSet) != len(self.data.currentStereotypeInfo):
                raise Exception("Error not all function signatures are unique within transformed document. Alter naming convention!")

            # Testing for non-unique function signatures.
            missingOrExtraFunctions = list(initialFunctionSigSet - currentFunctionSigSet)
            if len(missingOrExtraFunctions) != 0:
                hasMissingFunctions = True
                self.outputMissingFunctions(reportStrm)

            if not hasMissingFunctions:
                functionDataIndex = 0
                for functionData in zip(self.data.initialStereotypeInfo, self.data.currentStereotypeInfo):

                    # Testing Expected Vs. Actual
                    if functionData[0][0] != functionData[1][0]:
                        errMsg = """Mismatched function names @Index:{6}:
  Expected Function Name: {0}
  Actual Function Name: {1}

  Expected Stereotype: {2}
  Actual Stereotype: {3}

  Expected File: {4}
  Actual File: {5}
  """.format(
    functionData[0][0], functionData[1][0],
    functionData[0][1], functionData[1][1],
    functionData[0][2], functionData[1][2],
    functionDataIndex
)
                        self.data.testResultErrorText.append(errMsg)
                        reportStrm.write(errMsg)
                        continue

                    if functionData[0][1] != functionData[1][1]:
                        errMsg = """Mismatched function Stereotypes @Index:{6}:
  Expected Function Name: {0}
  Actual Function Name: {1}

  Expected Stereotype: {2}
  Actual Stereotype: {3}

  Expected File: {4}
  Actual File: {5}
  """.format(
    functionData[0][0], functionData[1][0],
    functionData[0][1], functionData[1][1],
    functionData[0][2], functionData[1][2],
    functionDataIndex
)
                        self.data.testResultErrorText.append(errMsg)
                        reportStrm.write(errMsg)
                    functionDataIndex += 0

            else:
                reportStrm.write("Unable to output functions with incorrect stereotypes due to previous errors.")
        
        # Getting a list of functions that are now missing from within the system.

        





        # unitTestInstance.assertEqual(
        #     expectedData["matchesWithAStereotype"],
        #     len(matches),
        #     "Incorrect # of stereotypes. Expected: {0} Actual: {1}".format(expectedData["matchesWithAStereotype"], len(matches))
        # )
        
        # for testData in zip(matches, expectedData["functionInfo"]):

        #     nameResult = testData[0].xpath("src:name/src:name[last()]/text()", namespaces=xmlNamespaces)
        #     unitTestInstance.assertEqual(testData[1][0], nameResult[0], "Incorrect function name. Expected: {0} Actual: {1}".format(testData[1][0], nameResult[0]))
        #     unitTestInstance.assertIsNotNone(testData[0], "Invalid matched stereotype function.")
        #     stereotypeMatch = stereotypeExtractingRe.search(testData[0].getprevious().text)
        #     if stereotypeMatch == None:
        #         unitTestInstance.assertIsNone(
        #             testData[1],
        #             "This may indicate an invalid match. Stereotype has invalid comment before itself that is not recognized as a stereotype: {0} ".format(testData[0].getprevious().text)
        #         )
        #     else:
        #         methodStereotypes = [x.lower() for x in stereotypeMatch.group("stereotypes").strip().split(" ")]
        #         unitTestInstance.assertSetEqual(
        #             set(testData[1][1]),
        #             set(methodStereotypes),
        #             "Mismatched between expected and actual stereotypes. Expected: {0}. Actual: {1}. FunctionName: {2}".format(testData[1][1], methodStereotypes, nameResult[0])
        #         )

        # newDoc = readable
        # outputDocumentPathFilePrefix = os.path.split(testFile)[1]

        # reportFilePath = os.path.join(DataFolderName, outputDocumentPathFilePrefix +".report.txt")
        # try:
        #     reportStrm = open(reportFilePath, "w")
        #     for func in oldStereotypedFunctionInfo:
        #         reportStrm.write(str(func[0]))
        #         reportStrm.write("| ")
        #         reportStrm.write(str(func[1]))
        #         reportStrm.write("\n")
        #     reportStrm.close()
        # except Exception as e:
        #     print func[1]
        #     print func[0]
        # # print oldStereotypedFunctionInfo
        # sys.stdout.flush()
    def outputMissingFunctions(self, reportStrm):
        reportStrm.write("Missing Function Report")

        # Missing Function Report.
        initialFunctionSigSet = set([x[0] for x in self.data.initialStereotypeInfo])
        currentFunctionSigSet = set([x[0] for x in self.data.currentStereotypeInfo])
        missingFunctiions = list(initialFunctionSigSet- currentFunctionSigSet)
        for f in missingFunctiions:
            reportStrm.write("  {0}\n".format(f))