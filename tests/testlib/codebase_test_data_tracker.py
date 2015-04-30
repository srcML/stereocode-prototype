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
from srcml.xslt import *
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
        self.mismatchStereotypeResults = []

DataFolderName = "archive_test_data/reports"
CodeOutputFolderName = "archive_test_data/reports/Code"

class CodeBaseTestDataTracker:
    def __init__(self):
        self.testData = []
        self.data = None

    def runTest(self, testFile, knownMacros):
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
        # print "Testing"

        print "  Reprocessing with srcML into srcML"
        sys.stdout.flush()

        functionTemplateFix = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:src="http://www.sdml.info/srcML/src"
>
<xsl:output omit-xml-declaration="no"/>

<xsl:template match="node() | @*">
    <xsl:copy>
        <xsl:apply-templates select="node() | @*"/>
    </xsl:copy>
</xsl:template>

<xsl:template match="src:function[src:template][src:comment]">
    <xsl:apply-templates select="src:comment"/>
    <xsl:copy>
        <xsl:apply-templates select="child::node()[not(self::src:comment)]"/>
    </xsl:copy>
    

</xsl:template>

</xsl:stylesheet>"""
        
        outputDocumentPathFilePrefix = os.path.split(testFile)[1]
        resrcMLedOutputFilePath = os.path.join(DataFolderName, outputDocumentPathFilePrefix + ".tempfile.xml")
        templateFixFilePath = os.path.join(DataFolderName, outputDocumentPathFilePrefix + ".templateFix.xml")
        stereotypedOutputDocPath = os.path.join(DataFolderName, outputDocumentPathFilePrefix + ".stereotyped.xml")
        extractFileNameDict = dict({
            # "Dev_Poll_Reactor.cpp":0,
            # "Local_Locator.cpp":0,
            # "OS_NS_Thread.cpp":0,
            # "OS_NS_sys_socket.cpp":0,
            # "Process.cpp":0,
            # "Protocol.h":0,
            # "SSL_Context.cpp":0
            # "CDR_Stream.cpp":0
            }
        )
        extractedNamesPostStereotypedDict = dict(extractFileNameDict)
        counter = 0
        with readable_archive(readable_archive_settings(), filename=testFile) as reader:
            writableSettings = writable_archive_settings(default_language=LANGUAGE_CXX, macros=knownMacros)
            writableSettings.parser_options |= OPTION_CPPIF_CHECK | OPTION_XML_DECL
            with writable_archive(writableSettings, filename=resrcMLedOutputFilePath) as outputArch:
                currentUnit = reader.read()
                while currentUnit != None:
                    if (counter % 500) == 0:
                        print "    Processed file count: ", counter
                        sys.stdout.flush()
                    # print currentUnit.filename
                    outputUnit = outputArch.create_unit(filename=currentUnit.filename)
                    source_code=currentUnit.unparse()
                    if currentUnit.filename in  extractFileNameDict:
                        temp = os.path.splitext(currentUnit.filename)
                        outputFileName = "{0}_{1}{2}".format(temp[0], extractFileNameDict[currentUnit.filename], temp[1])
                        extractFileNameDict[currentUnit.filename] += 1
                        print "  Processing problematic markup: ", outputFileName
                        problematicMarkupFileName = os.path.join(CodeOutputFolderName, outputFileName)
                        tempStrm = open(problematicMarkupFileName, "w")
                        tempStrm.write(source_code)
                        tempStrm.close()
                        with writable_archive(writable_archive_settings(xml_encoding="UTF-8", default_language=LANGUAGE_CXX, macros=knownMacros), filename=problematicMarkupFileName+".xml") as codeOutputArch:
                            codeOutputUnit = codeOutputArch.create_unit(filename=currentUnit.filename)
                            codeOutputUnit.parse(source_code=source_code)
                            codeOutputArch.write(codeOutputUnit)

                    outputUnit.parse(source_code=source_code)
                    outputArch.write(outputUnit)
                    currentUnit = reader.read()
                    counter += 1
            print "    Total Processed File Count: ", counter

        # Loading current document for processing
        print "  Transforming Document"
        sys.stdout.flush()
        p = et.XMLParser(huge_tree=True)
        tree = et.parse(resrcMLedOutputFilePath, parser=p)
        parseStyleSheetTest = et.XSLT(et.XML(functionTemplateFix))
        transformedTree = parseStyleSheetTest(tree)
        for entry in parseStyleSheetTest.error_log:
            print entry
        # print "\n".join(parseStyleSheetTest.error_log)
        treeStrm = open(templateFixFilePath, "w")
        transformedTree.write(treeStrm)
        treeStrm.close()

        # Loading current document for processing
        print "  Loading Initial Document"
        sys.stdout.flush()

        oldStereotypedFunctionInfo = extractStereotypesFromDocument(templateFixFilePath)
        self.data.initialStereotypeInfo = oldStereotypedFunctionInfo
        self.data.initialHistogram = buildHistogram(oldStereotypedFunctionInfo)
        
        removeCommentsXslt = """<?xml version="1.0" encoding="utf-8"?>
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



        removeCommentsDoc = et.XSLT(et.XML(removeCommentsXslt))
        print >> sys.stderr, "  Loading archive for additional processing"
        documentToTransform = et.parse(templateFixFilePath)
        print >> sys.stderr, "  Removing Comments and Redocumenting source code"
        transformedDocument = stereocode.stereocodeDoc(removeCommentsDoc(documentToTransform))
        transformedDocument.write(stereotypedOutputDocPath)

        if any([(x[1] > 0) for x in extractFileNameDict.items()]):
            with readable_archive(readable_archive_settings(), filename=stereotypedOutputDocPath) as reader:
                for currentUnit in reader:
                    if currentUnit.filename in extractedNamesPostStereotypedDict:
                        temp = os.path.splitext(currentUnit.filename)
                        outputFileName = "actual__{0}_{1}{2}".format(temp[0], extractedNamesPostStereotypedDict[currentUnit.filename], temp[1])
                        extractedNamesPostStereotypedDict[currentUnit.filename] += 1
                        print "  Outputting Reporcessed source code file: ", outputFileName
                        problematicMarkupFileName = os.path.join(CodeOutputFolderName, outputFileName)
                        currentUnit.unparse(filename=problematicMarkupFileName)
                        outputXmlStrm = open(problematicMarkupFileName + ".xml", "w")
                        outputXmlStrm.write(currentUnit.get_standalone_xml())
                        outputXmlStrm.close()

        print >> sys.stderr, "  Comment Removal Entries"
        for entry in removeCommentsDoc.error_log:
            print >> sys.stderr, "    %s" % entry

        print >> sys.stderr, "  Stereotype Log Entries"
        for entry in stereocode.stereocodeDoc.error_log:
            print >> sys.stderr, "    %s" % entry

        # xsltInputBuffer = memory_buffer()
        # xsltInputBuffer.load_from_string(removeCommentsXslt)
        # with readable_archive(readable_archive_settings(xsltransformations=[xsltransform(buffer=xsltInputBuffer), xsltransform(filename=stereocode.stereocodeXsltFilePath)]), filename=templateFixFilePath) as reader:
        #     with writable_archive(writable_archive_settings(), filename=stereotypedOutputDocPath) as outputArchive:
        #         reader.xslt.apply(outputArchive)



        print >> sys.stderr, "  Extracting new stereotype information from document"

        newStereotypeInfo = extractStereotypesFromDocument(stereotypedOutputDocPath)

        self.data.currentStereotypeInfo = newStereotypeInfo
        self.data.currentHistogram = buildHistogram(newStereotypeInfo)

        print "  Analyzing Stereotype document"
        sys.stdout.flush()


        # Comparing Expected and actual to see if they
        # are the same or not.
        
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

        fullStereotypeHistogramListing = list(set(self.data.initialHistogram.keys() + self.data.currentHistogram.keys()))
        # Outputting relative to what's missing from the current histogram
        reportStrm.write("+ Means that there are extra entries within the currentHistogram and - means missing entries from current histogram\n")
        for stereotype in fullStereotypeHistogramListing:
            if stereotype in self.data.initialHistogram and stereotype in self.data.currentHistogram:
                difference = self.data.currentHistogram[stereotype] - self.data.initialHistogram[stereotype]
                reportStrm.write("{0:>6}: {1}\n".format(difference if difference < 0 else "+" +str(difference), stereotype))

            elif stereotype not in self.data.initialHistogram and stereotype in self.data.currentHistogram:
                reportStrm.write("+{0:>6}: {1}\n".format(self.data.currentHistogram[stereotype], stereotype))
            elif stereotype in self.data.initialHistogram and stereotype not in self.data.currentHistogram:
                reportStrm.write("-{0:>6}: {1}\n".format(self.data.initialHistogram[stereotype], stereotype))
            else: 
                raise Exception("This should never happen.")

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
                    errMsg = "Mismatched histogram ordering @Index: {2}:\n  Expected: {0}\n  Actual: {1}\n".format(histData[0][0],  histData[1][0], histogramIndex)
                    reportStrm.write(errMsg)
                    self.data.testResultErrorText.append(errMsg)
                if histData[0][1] != histData[1][1]:
                    hasHistogramError = True
                    errMsg = "Mismatched histogram item count @Index: {4}:\n  Expected: {0}: {1}\n  Actual: {2}: {3}\n".format(
                        histData[0][0], histData[0][1],
                        histData[1][0], histData[1][1],
                        histogramIndex
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

        # Reporting extra functions
        # Doing a set difference to see if the same functions exist within both
        # sets of function info.
        # ---------------------------------------------------------------------------
        #                          !!!!Start working here!!!!!
        # ---------------------------------------------------------------------------

        def buildFunctionBySigDict(stereotypeDataInput):
            ret = dict()
            for stereotypeInfo in stereotypeDataInput:
                functionCounter = 0
                nextStereotypeName = stereotypeInfo[0]
                while nextStereotypeName in ret:
                    functionCounter += 1
                    nextStereotypeName = nextStereotypeName[0] + "_{0}".format(functionCounter)
                ret.update({nextStereotypeName: stereotypeInfo})
            return ret

        initialFunctionBySig = buildFunctionBySigDict(self.data.initialStereotypeInfo)
        currentFunctionBySig = buildFunctionBySigDict(self.data.currentStereotypeInfo)
        assert len(initialFunctionBySig) == len(self.data.initialStereotypeInfo), "Incorrect # of functions in dictionary"
        assert len(currentFunctionBySig) == len(self.data.currentStereotypeInfo), "Incorrect # of functions in dictionary"

        # Computing differences in stereotype between current and initial stereotype data
        if len(self.data.currentStereotypeInfo) >= len(self.data.initialStereotypeInfo):
            for currentData in initialFunctionBySig.items():
                if currentData[0] not in currentFunctionBySig:
                    raise Exception("Invalid function signature located. Signature: {0}  stereotype: {1} File: {2} Line In File: {3} Line in Arch: {4}".format(*currentData[1]))
                if currentData[1][1] != initialFunctionBySig[currentData[0]][1]:
                    self.data.mismatchStereotypeResults.append((currentData[1], currentData[1], initialFunctionBySig[currentData[0]]))
                del initialFunctionBySig[currentData[0]]
            # Sorting relative to the file name so that all entries can be easily output using the file name
            # to do so.
            print >> sys.stderr, "  Reached Checking functions with mismatched stereotypes "
            self.data.mismatchStereotypeResults = sorted(self.data.mismatchStereotypeResults, key=lambda x:x[3])
            if len(self.data.mismatchStereotypeResults) > 0:
                reportStrm.write("\n\n\n" + (80*"~") + "Functions with mismatched stereotypes. Count: {0}\n".format(len(self.data.mismatchStereotypeResults)) + (80*"~") + "\n\n\n")
                currentFileName = None
                for stereotypeCmp in self.data.mismatchStereotypeResults:
                    if currentFileName != stereotypeCmp[1][3]:
                        currentFileName = stereotypeCmp[1][3]
                        reportStrm.write("{0}\n".format(currentFileName))
                    if stereotypeCmp[1][3] != stereotypeCmp[2][3]:
                        raise Exception("""Mismatched filenames between functions that are supposed to be the same.
Expected:
    Signature: {0}  stereotype: {1} File: {2} Line In File: {3} Line in Arch: {4}
Actual:
    Signature: {5}  stereotype: {6} File: {7} Line In File: {8} Line in Arch: {9}""".format(
                                *[x for y in stereotypeCmp[1:] for x in y]
                            )
                        )
                    else:
                        reportStrm.write("""
    Function: {0}
        Expected:
          stereotype: {1}
          File: {3}
          Line In File: {4}
          Line in Arch: {5}
        Actual:
          Signature: {6}
          stereotype: {7}
          File: {8}
          Line In File: {9}
          Line in Arch: {10}
""".format(stereotypeCmp[0], *[x for y in stereotypeCmp[1:] for x in y]))
            else:
                print "  Good NEWS! No mismatched stereotypes!"
        else:
            print >> sys.stderr, "WARNING: Didn't locate all functions correctly."

        # if len(initialFunctionSigSet) != len(self.data.initialStereotypeInfo):
        #     raise Exception("WARNING INITIAL STEREOTYPE HAS NON UNIQUE FUNCTION NAME!")
        #     temp = []
        #     currentFilename = self.data.initialStereotypeInfo[0][2]
        #     for funcInfo in self.data.initialStereotypeInfo:
        #         if currentFilename != funcInfo[2]:
        #             currentFilename = funcInfo[2]
        #         temp.append((funcInfo[2] + " " + funcInfo[0], funcInfo[1], funcInfo[2]))
        #     self.data.initialStereotypeInfo = temp
        #     initialFunctionSigSet = set([x[0] for x in self.data.initialStereotypeInfo])
        #     if len(initialFunctionSigSet) != len(self.data.initialStereotypeInfo):
        #         reportStrm.write("WARNING: two functions with the same name within the same file.")
        #         # raise Exception("Error not all function signatures are unique within initial document.")

        # if len(currentFunctionSigSet) != len(self.data.currentStereotypeInfo):
        #     raise Exception("WARNING INITIAL STEREOTYPE HAS NON UNIQUE FUNCTION NAME!")
        #     temp = []
        #     currentFilename = self.data.currentStereotypeInfo[0][2]
        #     for funcInfo in self.data.currentStereotypeInfo:
        #         if currentFilename != funcInfo[2]:
        #             currentFilename = funcInfo[2]
        #         temp.append((funcInfo[2] + " " + funcInfo[0], funcInfo[1], funcInfo[2]))
        #     self.data.currentStereotypeInfo = temp
        #     currentFunctionSigSet = set([x[0] for x in self.data.currentStereotypeInfo])
        #     if len(currentFunctionSigSet) != len(self.data.currentStereotypeInfo):
        #         reportStrm.write("WARNING: two functions with the same name within the same file.")

#             # Testing for non-unique function signatures.
#             missingOrExtraFunctions = list(initialFunctionSigSet - currentFunctionSigSet)
#             if len(missingOrExtraFunctions) != 0:
#                 hasMissingFunctions = True
#                 self.outputMissingFunctions(reportStrm)

#             if not hasMissingFunctions:
#                 functionDataIndex = 0
#                 for functionData in zip(self.data.initialStereotypeInfo, self.data.currentStereotypeInfo):

#                     # Testing Expected Vs. Actual
#                     if functionData[0][0] != functionData[1][0]:
#                         errMsg = """Mismatched function names @Index:{6}:
#   Expected Function Name: {0}
#   Actual Function Name: {1}

#   Expected Stereotype: {2}
#   Actual Stereotype: {3}

#   Expected File: {4}
#   Actual File: {5}
#   """.format(
#     functionData[0][0], functionData[1][0],
#     functionData[0][1], functionData[1][1],
#     functionData[0][2], functionData[1][2],
#     functionDataIndex
# )
#                         self.data.testResultErrorText.append(errMsg)
#                         reportStrm.write(errMsg)
#                         continue

#                     if functionData[0][1] != functionData[1][1]:
#                         errMsg = """Mismatched function Stereotypes @Index:{6}:
#   Expected Function Name: {0}
#   Actual Function Name: {1}

#   Expected Stereotype: {2}
#   Actual Stereotype: {3}

#   Expected File: {4}
#   Actual File: {5}
#   """.format(
#     functionData[0][0], functionData[1][0],
#     functionData[0][1], functionData[1][1],
#     functionData[0][2], functionData[1][2],
#     functionDataIndex
# )
#                         self.data.testResultErrorText.append(errMsg)
#                         reportStrm.write(errMsg)
#                     functionDataIndex += 0

#             else:
#                 reportStrm.write("Unable to output functions with incorrect stereotypes due to previous errors.")
        
        # os.remove(stereotypedOutputDocPath)
        os.remove(resrcMLedOutputFilePath)
        os.remove(templateFixFilePath)



    def outputMissingFunctions(self, reportStrm):
        invalidCharacterReplacement = "?"
        reportStrm.write("Missing Function Report\n")

        # Missing Function Report.
        initialFunctionSigSet = set([x[0] for x in self.data.initialStereotypeInfo])
        currentFunctionSigSet = set([x[0] for x in self.data.currentStereotypeInfo])
        missingFunctions = list(initialFunctionSigSet - currentFunctionSigSet)


        # for f in missingFunctions:
        #     try:
        #         reportStrm.write("  {0}\n".format(f))
        #     except UnicodeError as e:
        #         # print "Encountered UnicodeError Performing replacement with ~ character."
        #         reportStrm.write("  " + " ".join([c if ord(c)< 128 else invalidCharacterReplacement for c in f]))

        #Sorting out which functions are missing from which archive.
        functionsNotFound = []
        extraFunctionsFound = []
        for f in set(missingFunctions) | set(currentFunctionSigSet - initialFunctionSigSet):
            if f in initialFunctionSigSet:
                functionsNotFound.append(f)
            else:
                extraFunctionsFound.append(f)
                
        reportStrm.write("\n\n")
        reportStrm.write("Missed Functions. Count: {0}\n".format(len(functionsNotFound)))
        initialStereotypeLookUp = {x[0]: x for x in self.data.initialStereotypeInfo}

        functionsNotFound = sorted([initialStereotypeLookUp[f] for f in functionsNotFound], key = lambda x: x[2])
        currentFileName = None
        for f in functionsNotFound:
            if currentFileName != f[2]:
                reportStrm.write("\n" + f[2] + "\n")
                currentFileName = f[2]
            try:
                reportStrm.write("  {0}".format(f[0]))
            except UnicodeError as e:
                reportStrm.write(" ".join([c if ord(c)< 128 else invalidCharacterReplacement for c in f[0]]))
            reportStrm.write(": Expected Stereotypes: {0} FileName: {1}:{2} Archive Line#: {3}\n".format(*f[1:]))

        reportStrm.write("\n\nExtra/Newly Located Functions Located. Count: {0}\n".format(len(extraFunctionsFound)))
        currentStereotypeLookUp = {x[0]: x for x in self.data.currentStereotypeInfo}
        extraFunctionsFound = sorted([currentStereotypeLookUp[f] for f in extraFunctionsFound], key = lambda x: x[2])


        for f in extraFunctionsFound:
            if currentFileName != f[2]:
                reportStrm.write("\n" + f[2] + "\n")
                currentFileName = f[2]
            try:
                reportStrm.write("  {0}".format(f[0]))
            except UnicodeError as e:
                reportStrm.write(" ".join([c if ord(c)< 128 else invalidCharacterReplacement for c in f[0]]))
            reportStrm.write(": Stereotypes: {0} FileName: {1}:{2} Archive Line#: {3}\n".format(*f[1:]))