##
# @file xslt_utils.py
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

import stereocode, lxml, lxml.etree as et, re, os, os.path, shutil, sys, StringIO, lxml.sax as lsax
from xml.sax.handler import ContentHandler
import xml.sax as sax
from srcml import *

# from operator import itemgetter, attrgetter, methodcaller
xmlNamespaces = dict(src="http://www.srcML.org/srcML/src", cpp="http://www.srcML.org/srcML/cpp")
stereotypeExtractingRe = re.compile(r"@stereotype (?P<stereotypes>[^\*]*)")
# print >> sys.stderr, stereotypeExtractingRe.pattern

def executeTransform(xmlDocument, xsltDocument):
    """
    This will need to do more in the future like setting up possible parameters
    and register other possible extension functionality associated with the
    XSLT document.
    """
    return xsltDocument(xmlDocument)

def executeAndTestTransform(unitTestInstance, xmlDocument, xsltDocument, expectedData, printTrasformedDoc=False):
    try:
        resultingDoc = executeTransform(xmlDocument, xsltDocument)
        if len(xsltDocument.error_log) > 0:
            print >> sys.stderr, "Error Log entries:"
            for entry in xsltDocument.error_log:
                print >> sys.stderr, """    Line: {0} Col: {1} Domain: {2} Level: {3} Level Name: {4} Type: {5} Type Name: {6} Message: {7}""".format(entry.line, entry.column, entry.domain, entry.level, entry.level_name, entry.type, entry.type_name, entry.message)
        if printTrasformedDoc:
            print et.tostring(resultingDoc)
    except:
        print >> sys.stderr, "Failed to execute transformation"
        raise

    matches = []
    try:
        matches = resultingDoc.xpath(
            "//src:function[preceding-sibling::*[1][self::src:comment]]",
            namespaces=xmlNamespaces
        )
        unitTestInstance.assertEqual(
            expectedData["matchesWithAStereotype"],
            len(matches),
            "Incorrect # of stereotypes. Expected: {0} Actual: {1}".format(expectedData["matchesWithAStereotype"], len(matches))
        )
        
        for testData in zip(matches, expectedData["functionInfo"]):

            nameResult = testData[0].xpath("src:name/src:name[last()]/text()", namespaces=xmlNamespaces)
            unitTestInstance.assertEqual(testData[1][0], nameResult[0], "Incorrect function name. Expected: {0} Actual: {1}".format(testData[1][0], nameResult[0]))
            unitTestInstance.assertIsNotNone(testData[0], "Invalid matched stereotype function.")
            stereotypeMatch = stereotypeExtractingRe.search(testData[0].getprevious().text)
            if stereotypeMatch == None:
                unitTestInstance.assertIsNone(
                    testData[1],
                    "This may indicate an invalid match. Stereotype has invalid comment before itself that is not recognized as a stereotype: {0} ".format(testData[0].getprevious().text)
                )
            else:
                methodStereotypes = [x.lower() for x in stereotypeMatch.group("stereotypes").strip().split(" ")]
                unitTestInstance.assertSetEqual(
                    set(testData[1][1]),
                    set(methodStereotypes),
                    "Mismatched between expected and actual stereotypes. Expected: {0}. Actual: {1}. FunctionName: {2}".format(testData[1][1], methodStereotypes, nameResult[0])
                )
    except:
        print >> sys.stderr, "Failed to test stereotype data"
        # print "transformed document"
        # print et.tostring(resultingDoc)

        # print "\n\n\nMatches: "
        # for m in matches:
        #     print et.tostring(m)
        raise


def quickDumpFunctionStereotypeInfo(xmlDocument, xsltDocument,):

    try:
        resultingDoc = executeTransform(xmlDocument, xsltDocument)
        print >> sys.stderr,  et.tostring(resultingDoc)
        if len(xsltDocument.error_log) >0:
            print >> sys.stderr, xsltDocument.error_log
    except:
        print "Failed to execute transformation"
        raise

    matches = []
    try:
        matches = resultingDoc.xpath(
            "//src:function[preceding-sibling::*[1][self::src:comment]]",
            namespaces=xmlNamespaces
        )
        print >> sys.stderr, "Number of Functions located: {0}".format(len(matches))

    except:
        print >> sys.stderr,  "Failed to test stereotype data"
        # print "transformed document"
        # print et.tostring(resultingDoc)

        # print "\n\n\nMatches: "
        # for m in matches:
        #     print et.tostring(m)
        raise





class ExtFunctions:
    def unitIsCPPFile(self, ctxt, arg):
        fileExtension = os.path.splitext(arg[0].get("filename"))[-1].lower()[1:]
        ret = fileExtension == "cxx" or fileExtension == "cpp" or fileExtension == "hpp" or fileExtension == "hxx" or fileExtension == "h"

        return ret

    def funcHasStereotype(self, ctxt, arg):
        nodePrevToFunc = arg[0].getprevious()
        if nodePrevToFunc == None:
            return False
        if et.QName(nodePrevToFunc.tag).localname == "comment":
            return stereotypeExtractingRe.search(nodePrevToFunc.text) != None
        else:
            return False

def _getStereotype(funcNode):
    stereotypeMatch = stereotypeExtractingRe.search(funcNode.getprevious().text)
    if stereotypeMatch == None:
        raise Exception("Error Locating Stereotype data. Erring comment: {0}".format(funcNode.getprevious().text))
    else:
        return [x.lower() for x in stereotypeMatch.group("stereotypes").strip().split(" ")]


class FunctionSignatureExtractor(ContentHandler):
    def __init__(self):
        self.continueReading = True
        self.text = []
        self.isComment = False

    def startElementNS(self, qname, name, attributes):
        if qname[1] == "block":
            self.continueReading = False
        elif qname[1] == "comment":
            self.isComment = True

    def endElementNS(self, qname, name):
        if qname[1] == "comment":
            self.isComment = False

    def characters(self, data):
        if self.isComment:
            return
        if self.continueReading:
            nextText = data.strip()
            if nextText != "":
                self.text.append(nextText)

    def run(self, startingElement):
        lsax.saxify(startingElement, self)
        result = " ".join(self.text)
        self.text = []
        self.continueReading = True
        return result
_sigExtractorUtility = FunctionSignatureExtractor()

def _getNormalizedFunctionSig(functionElement):
    return _sigExtractorUtility.run(functionElement)

def generateTestReport(processedArchive, reportFolder):

    # Extension function helpers
    # ns = et.FunctionNamespace(None)

    helperModule = ExtFunctions()
    functions = {'unitIsCPPFile':'unitIsCPPFile', 'funcHasStereotype':'funcHasStereotype'}
    extensions = et.Extension(helperModule, functions)
    namespaces = {'src':'http://www.srcML.org/srcML/src', 'cpp':'http://www.srcML.org/srcML/cpp'}
    evaluator = et.XPathEvaluator(processedArchive, namespaces=namespaces, extensions=extensions)


    # ns = et.FunctionNamespace(None)
    # ns['funcHasStereotype'] =  funcHasStereotype

    if os.path.exists(reportFolder):
        shutil.rmtree(reportFolder)
    os.mkdir(reportFolder)


    # The things to report about this archive.
    totalFileCount = 0
    CPPFileCount = 0
    classCount = 0 
    functionDeclCount = 0
    functionDefnCount = 0
    annotatedFunctionDeclCount = 0
    annotatedFunctionDefnCount = 0
    functionDeclStereotypeHistogram = dict()
    functionDefnStereotypeHistogram = dict()
    functionSigAndStereotype = []

    # Listing all C++ files within the archive.
    cppFileListing = evaluator("/src:unit/src:unit[unitIsCPPFile(.)]")
    CPPFileCount = len(cppFileListing)
    print >> sys.stderr, "CPP File Count: ", CPPFileCount
    sys.stdout.flush()

    # Getting the # of units within the archive.
    totalFileCount = int(evaluator("count(/src:unit/src:unit)"))
    print >> sys.stderr, "Total File Count: ", totalFileCount
    sys.stdout.flush()

    # Counting the # of structs + classes within all C++ files.
    classCount = int(evaluator("count(/src:unit/src:unit[unitIsCPPFile(.)]//src:class)"))
    structCount = int(evaluator("count(/src:unit/src:unit[unitIsCPPFile(.)]//src:struct)"))
    print >> sys.stderr, "Class Count: ", classCount
    print >> sys.stderr, "Struct Count: ", structCount
    sys.stdout.flush()

    # Counting function decl/def within files that CPP files.
    functionDeclCount = int(evaluator("count(/src:unit/src:unit[unitIsCPPFile(.)]//src:function_decl)"))
    print >> sys.stderr, "Function Declaration Count: ", functionDeclCount
    sys.stdout.flush()

    functionDefnCount = int(evaluator("count(/src:unit/src:unit[unitIsCPPFile(.)]//src:function)"))
    print >> sys.stderr, "Function Definition Count: ", functionDefnCount
    sys.stdout.flush()

    # # Counting annotated function decls & defs.
    print >> sys.stderr, "Attempting to count the # of annotated functions"
    sys.stdout.flush()

    collectedFunctionDefns = []
    functionSigAndStereotype = []
    for unit in cppFileListing:
        elementEvaluator = et.XPathElementEvaluator(unit, namespaces=namespaces, extensions=extensions)
        listOfFunctions = elementEvaluator(".//src:function[funcHasStereotype(.)]")
        collectedFunctionDefns += listOfFunctions 

        for func in listOfFunctions:
            stereotypes = _getStereotype(func)
            stereotypes = sorted(stereotypes)

            stereotypeKey = " ".join(stereotypes)
            funcEvaluator = et.XPathElementEvaluator(func, namespaces=namespaces, extensions=extensions)
            functionSigAndStereotype.append( (_getNormalizedFunctionSig(func), stereotypeKey, unit.get("filename")) )
            if stereotypeKey in functionDefnStereotypeHistogram:
                functionDefnStereotypeHistogram[stereotypeKey] += 1
            else:
                functionDefnStereotypeHistogram[stereotypeKey] = 1
    # annotatedFuncDecls = evaluator("/src:unit/src:unit[unitIsCPPFile(.)]//src:function_decl[funcHasStereotype(.)]") 
    # print "Annotated Function declarations: ", len(collectedFunctionsDecls)
    print >> sys.stderr, "# Of Annotated Function definitions: ", len(collectedFunctionDefns)


    temp = list(functionDefnStereotypeHistogram.items())
    temp = sorted(temp, key=lambda x: x[1])

    

    print >> sys.stderr, "\n".join([str(x) for x in temp])

    reportOutputPath = os.path.join(reportFolder, "functionStereotypeReport.txt")
    reportOutputStrm = open(reportOutputPath, "w")
    currentFile = ""
    for reportEntry in functionSigAndStereotype:
        if currentFile != reportEntry[2]:
            currentFile = reportEntry[2]
            reportOutputStrm.write("\n{0}\n".format(reportEntry[2]))
        reportOutputStrm.write( reportEntry[0])
        reportOutputStrm.write(", "  + reportEntry[1] + "\n")
    reportOutputStrm.close()



def generateStereotypeReportFromDoc(processedArchive):

    # Extension function helpers
    helperModule = ExtFunctions()
    functions = {'unitIsCPPFile':'unitIsCPPFile', 'funcHasStereotype':'funcHasStereotype'}
    extensions = et.Extension(helperModule, functions)
    namespaces = {'src':'http://www.srcML.org/srcML/src', 'cpp':'http://www.srcML.org/srcML/cpp'}
    evaluator = et.XPathEvaluator(processedArchive, namespaces=namespaces, extensions=extensions)

    # Listing all C++ files within the archive.
    cppFileListing = evaluator("/src:unit/src:unit[unitIsCPPFile(.)]")

    functionSigAndStereotype = []
    for unit in cppFileListing:
        elementEvaluator = et.XPathElementEvaluator(unit, namespaces=namespaces, extensions=extensions)
        listOfFunctions = elementEvaluator(".//src:function[funcHasStereotype(.)]")

        for func in listOfFunctions:
            stereotypes = _getStereotype(func)
            stereotypes = sorted(stereotypes)

            stereotypeKey = " ".join(stereotypes)
            funcEvaluator = et.XPathElementEvaluator(func, namespaces=namespaces, extensions=extensions)
            functionSigAndStereotype.append( (_getNormalizedFunctionSig(func), stereotypeKey, unit.get("filename")) )

    return functionSigAndStereotype


def buildHistogram(functionList):
    histogram = dict()
    for func in functionList:
        if func[1] in histogram:
            histogram[func[1]] += 1
        else:
            histogram[func[1]] = 1
    return histogram

STATE_UNIT_SEARCH = "Looking For Unit With FileName"
STATE_STEREOTYPE_REDOC_SEARCH = "Looking For Stereotype"
STATE_READING_COMMENT = "Reading Comment"
STATE_EXPECTING_FUNCTION = "Expecting function"
STATE_READING_FUNCTION = "Reading function Name"


# Tag Name Constants
unitTag = "unit"
commentTag = "comment"
functionTag = "function"
blockTag = "block"
escapeTag = "escape"

# Attribute constants
filenameAttr = "filename"
class StereotypeLocationTagError(Exception):
    def __init__(self, text, filename, lineNumber, archiveLineNumber):
        super(Exception, self).__init__(text)
        self.filename = filename
        self.lineNumber = lineNumber
        self.archiveLineNumber = archiveLineNumber

class FastStereotypeExtractor(sax.handler.ContentHandler):
    def __init__(self):
        self.inputFilePath = ""
        self.currentFileName = ""
        self.docLocator = None
        self.currentBuffer = StringIO.StringIO()
        self.currentStereotypeStr = ""
        self.functionStereotypeInfo = []
        self.state = STATE_UNIT_SEARCH
        self.readingFunctionNameDepth = 0
        self.functionLineNumber = 0
        self.unitLineNumber = 0
        self.skippingComment = False
        self.archiveLineNumber = 0

    def setDocumentLocator(self, locator):
        self.docLocator = locator

    def startElement(self, name, attrs):
        if self.state == STATE_UNIT_SEARCH:
            if name == "unit" or name == "macro-list":
                if filenameAttr in attrs:
                    self.currentFileName = attrs[filenameAttr]
                    self.state = STATE_STEREOTYPE_REDOC_SEARCH
                    self.unitLineNumber = self.docLocator.getLineNumber()
            else:
                raise Exception("Didn't locate expected element current Element Information. Name: {0} Attrs: {1}".format(name, attrs), self.currentFileName)


        elif self.state == STATE_STEREOTYPE_REDOC_SEARCH:
            if name == commentTag or name == "src:comment":
                self.state = STATE_READING_COMMENT
            
        elif self.state == STATE_READING_COMMENT:
            if name == escapeTag:
                return
            raise Exception("No tags should be encountered while reading comment because comment only consists of text with no children. Node Encountered: {0}".format(name), self.currentFileName)
        elif self.state == STATE_EXPECTING_FUNCTION:

            if name == functionTag or name =="friend":
                self.functionLineNumber = self.docLocator.getLineNumber() - self.unitLineNumber
                self.archiveLineNumber = self.docLocator.getLineNumber()
                self.state = STATE_READING_FUNCTION
                self.skippingComment = False
            elif name == commentTag or name == "src:comment":
                self.state = STATE_STEREOTYPE_REDOC_SEARCH
            else:
                raise StereotypeLocationTagError(
                    "Stereotype is missing function definition. Tag Name: {1} File: {0}:{3} Line #: {2}".format(self.currentFileName, name, self.docLocator.getLineNumber(), self.docLocator.getLineNumber() - self.unitLineNumber),
                    self.currentFileName,
                    self.docLocator.getLineNumber(),
                    self.docLocator.getLineNumber() - self.unitLineNumber
                )

        elif self.state == STATE_READING_FUNCTION:
            if name == commentTag:
                self.skippingComment = True
            if self.readingFunctionNameDepth == 0 and name == blockTag:
                self.state = STATE_STEREOTYPE_REDOC_SEARCH
                self.functionStereotypeInfo.append(
                    (
                        " ".join(self.currentBuffer.getvalue().split()),
                        self.currentStereotypeStr,
                        self.currentFileName,
                        self.functionLineNumber,
                        self.archiveLineNumber
                    )
                )
                # Renewing buffer for next use.
                self.currentBuffer.close()    
                self.currentBuffer = StringIO.StringIO()
                return
            self.readingFunctionNameDepth += 1


        else:
            raise Exception("Invalid/unknown state: {0}".format(self.state))

    def endElement(self, name):
        if self.state == STATE_UNIT_SEARCH:
            if name != "unit" and name != "macro-list":
                raise Exception("Invalid transition. Didn't locate a unit correctly")

        elif self.state == STATE_STEREOTYPE_REDOC_SEARCH:
            if name == "unit":
                self.state = STATE_UNIT_SEARCH

        elif self.state == STATE_READING_COMMENT:
            if name == escapeTag:
                return
            if name != commentTag and name != "src:comment":
                raise Exception("Invalid Transition didn't get expected end of comment. Tag: {0}".format(name), self.currentFileName)


            # Extract comment text, test to see if it's a stereotype
            # redocumentation comment transition states and
            # renew the buffer.
            commentStr = self.currentBuffer.getvalue()
            stereotypeMatch = stereotypeExtractingRe.search(commentStr)
            if stereotypeMatch == None:
                self.state = STATE_STEREOTYPE_REDOC_SEARCH
            else:
                self.currentStereotypeStr = " ".join(sorted([x.lower() for x in stereotypeMatch.group("stereotypes").strip().split(" ")]))
                self.state = STATE_EXPECTING_FUNCTION
            # Renewing buffer for next use.
            self.currentBuffer.close()    
            self.currentBuffer = StringIO.StringIO()

        elif self.state == STATE_EXPECTING_FUNCTION:
            pass
        elif self.state == STATE_READING_FUNCTION:
            if name == commentTag:
                self.skippingComment = False
            self.readingFunctionNameDepth -= 1
        else:
            raise Exception("Invalid/unknown state: {0}".format(self.state))


    def characters(self, content):
        if self.state == STATE_UNIT_SEARCH:
            pass
        elif self.state == STATE_STEREOTYPE_REDOC_SEARCH:
            pass
        elif self.state == STATE_READING_COMMENT:
            self.currentBuffer.write(content)
        elif self.state == STATE_EXPECTING_FUNCTION:
            pass
        elif self.state == STATE_READING_FUNCTION:
            if self.skippingComment:
                return
            outputStr = content
            if len(outputStr) > 0:
                self.currentBuffer.write(outputStr)
        else:
            raise Exception("Invalid/unknown state: {0}".format(self.state))

def reprocessAndExtractDocument(inputFilePath, outputDirectory, erroringFileName, knownMacros, outputFilePrefix = ""):
    """
    This is called when there's an error with one of the stereotypes. This function recovers
    the file that caused the error and outputs that file into archive_test_data/reports/Code
    with the supplied file name. The extraction is done using srcml.
    """
    counter = 0
    assert inputFilePath != "", "Incorrect file name"
    extractedFileMarkUpDict = dict()
    # archive_test_data/reports/Code
    with readable_archive(readable_archive_settings(), filename=inputFilePath) as reader:
        currentUnit = reader.read()
        while currentUnit != None:
            if currentUnit.filename == erroringFileName:
                temp = os.path.splitext(currentUnit.filename)
                if currentUnit.filename in extractedFileMarkUpDict:
                    extractedFileMarkUpDict[currentUnit.filename] += 1
                else:
                    extractedFileMarkUpDict[currentUnit.filename] = 0
                outputFileName = "{3}{0}_{1}{2}".format(temp[0], extractedFileMarkUpDict[currentUnit.filename], temp[1], outputFilePrefix)
                print >> sys.stderr, "  Processing problematic markup: ", outputFileName
                problematicMarkupFileName = os.path.join(outputDirectory, outputFileName)
                tempStrm = open(problematicMarkupFileName, "w")
                source_code = currentUnit.unparse()
                tempStrm.write(source_code)
                tempStrm.close()
                with writable_archive(writable_archive_settings(xml_encoding="UTF-8", default_language=LANGUAGE_CXX, macros=knownMacros), filename=problematicMarkupFileName+".xml") as codeOutputArch:
                    codeOutputUnit = codeOutputArch.create_unit(filename=currentUnit.filename)
                    codeOutputUnit.parse(source_code=source_code)
                    codeOutputArch.write(codeOutputUnit)
                    return 
            currentUnit = reader.read()
            counter += 1
        raise Exception("Unable to locate specified file name: {0}".format(erroringFileName))



def extractStereotypesFromDocument(pathToDoc):
    handler = FastStereotypeExtractor()
    handler.inputFilePath = pathToDoc
    sax.parse(pathToDoc, handler)
    return handler.functionStereotypeInfo