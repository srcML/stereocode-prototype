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

import stereocode, lxml, lxml.etree as et, re, os, os.path, shutil, sys, cStringIO, lxml.sax as lsax
from xml.sax.handler import ContentHandler

# from operator import itemgetter, attrgetter, methodcaller
xmlNamespaces = dict(src="http://www.sdml.info/srcML/src", cpp="http://www.sdml.info/srcML/cpp")
stereotypeExtractingRe = re.compile(r"@stereotype (?P<stereotypes>[^\*]*)")

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
            print "Error Log entries:"
            for entry in xsltDocument.error_log:
                print """    Line: {0} Col: {1} Domain: {2} Level: {3} Level Name: {4} Type: {5} Type Name: {6} Message: {7}""".format(entry.line, entry.column, entry.domain, entry.level, entry.level_name, entry.type, entry.type_name, entry.message)
        if printTrasformedDoc:
            print et.tostring(resultingDoc)
    except:
        print "Failed to execute transformation"
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
        print "Failed to test stereotype data"
        # print "transformed document"
        # print et.tostring(resultingDoc)

        # print "\n\n\nMatches: "
        # for m in matches:
        #     print et.tostring(m)
        raise


def quickDumpFunctionStereotypeInfo(xmlDocument, xsltDocument,):

    try:
        resultingDoc = executeTransform(xmlDocument, xsltDocument)
        print et.tostring(resultingDoc)
        if len(xsltDocument.error_log) >0:
            print xsltDocument.error_log
    except:
        print "Failed to execute transformation"
        raise

    matches = []
    try:
        matches = resultingDoc.xpath(
            "//src:function[preceding-sibling::*[1][self::src:comment]]",
            namespaces=xmlNamespaces
        )
        print "Number of Functions located: {0}".format(len(matches))
        
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
    except:
        print "Failed to test stereotype data"
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
        # if ret:
        #     print "Processing file: ", arg[0].get("filename")
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

    def startElementNS(self, qname, name, attributes):
        # print name
        if qname[1] == "block":
            self.continueReading = False

    def characters(self, data):
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
    # print dir(helperModule)
    functions = {'unitIsCPPFile':'unitIsCPPFile', 'funcHasStereotype':'funcHasStereotype'}
    extensions = et.Extension(helperModule, functions)
    namespaces = {'src':'http://www.sdml.info/srcML/src', 'cpp':'http://www.sdml.info/srcML/cpp'}
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
    print "CPP File Count: ", CPPFileCount
    sys.stdout.flush()

    # Getting the # of units within the archive.
    totalFileCount = int(evaluator("count(/src:unit/src:unit)"))
    print "Total File Count: ", totalFileCount
    sys.stdout.flush()

    # Counting the # of structs + classes within all C++ files.
    classCount = int(evaluator("count(/src:unit/src:unit[unitIsCPPFile(.)]//src:class)"))
    structCount = int(evaluator("count(/src:unit/src:unit[unitIsCPPFile(.)]//src:struct)"))
    print "Class Count: ", classCount
    print "Struct Count: ", structCount
    sys.stdout.flush()

    # Counting function decl/def within files that CPP files.
    functionDeclCount = int(evaluator("count(/src:unit/src:unit[unitIsCPPFile(.)]//src:function_decl)"))
    print "Function Declaration Count: ", functionDeclCount
    sys.stdout.flush()

    functionDefnCount = int(evaluator("count(/src:unit/src:unit[unitIsCPPFile(.)]//src:function)"))
    print "Function Definition Count: ", functionDefnCount
    sys.stdout.flush()

    # # Counting annotated function decls & defs.
    print "Attempting to count the # of annotated functions"
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
    print "# Of Annotated Function definitions: ", len(collectedFunctionDefns)


    temp = list(functionDefnStereotypeHistogram.items())
    temp = sorted(temp, key=lambda x: x[1])

    

    print "\n".join([str(x) for x in temp])

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
    # print functionDeclStereotypeHistogram
    # print functionDefnStereotypeHistogram
    # sys.stdout.flush()

