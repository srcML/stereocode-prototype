##
# @file test_stereotype_xslt.py
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


import unittest, lxml.etree as et, lxml
from stereocode import *
from testlib import *

class TestStereotypeXslt(unittest.TestCase):
    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    def test_basicXslt(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype":2,
            "functionInfo":
            [
                ("match1", ["get", "collaborator"]),
                ("match2", ["nonconstget"])
            ]
        })

    @srcMLifyCode("tests/test_data/stereotype/command.cpp")
    def test_commandTest(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 4,
            "functionInfo":
            [
                ("sort", ["command", "stateless"]),
                ("f", ["command"]),
                ("f2", ["stateless"]),
                ("f3", ["command"]),
            ]
        })

    @srcMLifyCode("tests/test_data/stereotype/empty.cpp")
    def test_empty(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 7,
            "functionInfo":
            [
                ("n1", ["collaborator", "empty"]),
                ("n2", ["collaborator", "empty"]),
                ("n3", ["collaborator", "empty"]),
                ("n5", ["collaborator", "empty"]),
                ("n6", ["collaborator", "empty"]),
                ("n7", ["collaborator", "empty"]),
                ("n8", [ "empty"]),
            ]
        })


    @srcMLifyCode("tests/test_data/stereotype/command-collaborator.cpp")
    def test_CommandCollaborator(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 2,
            "functionInfo":
            [
                ("findWhite", ["unclassified"]),
                ("findWhite", ["unclassified"]),
            ]
        })




    @srcMLifyCode("tests/test_data/xslt_functions/writeto.cpp")
    def test_writTo(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 6,
            "functionInfo":
            [
                ("updateGuess1", ["collaborator"]),
                ("updateGuess2", ["set", "collaborator"]),
                ("updateGuess3", ["collaborational-command","collaborator"]),
                ("updateGuess4", ["collaborational-command", "collaborator"]),
                ("updateGuess5", ["collaborator"]),
                ("updateGuess6", ["collaborational-command", "collaborator"]),

            ]
        })


    @srcMLifyCode("tests/test_data/xslt_functions/file.cpp")
    def test_filecpp(self, tree):
        """
        Not sure what this is testing exactly.
        """
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 6,
            "functionInfo":
            [
                ("append", ["collaborator"]),
                ("read", ["collaborator"]),
                ("compareItems", ["collaborator"]),
                ("newItem", ["nonconstget", "collaborator"]),
                ("readLink", ["collaborational-property", "collaborator"])
            ]
        })


    @srcMLifyCode("tests/test_data/stereotype/newset.cpp")
    def test_newSetStereotypeTest(self, tree):
        """
        Not sure what this is testing exactly.
        """
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 1,
            "functionInfo":
            [
                ("f", ["set"])
            ]
        })


    @srcMLifyCode("tests/test_data/stereotype/problem_1.cpp")
    def test_problemOneTest(self, tree):
        """
        Not sure what this is testing exactly.
        """
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 2,
            "functionInfo":
            [
                ("findWhite", ["unclassified"]),
                ("findWhite", ["unclassified"])
            ]
        })

    @srcMLifyCode("tests/test_data/stereotype/problem_2.cpp")
    def test_problemTwoTest(self, tree):
        """
        Not sure what this is testing exactly.
        """
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 1,
            "functionInfo":
            [
                ("isLeap", ['command', 'collaborator'])
            ]
        })


    @srcMLifyCode("tests/test_data/xslt_functions/t1.cpp")
    def test_t1(self, tree):
        """
        Not sure what this is testing exactly.
        """
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 1,
            "functionInfo":
            [
                ("foo", ['set', 'collaborator'])
            ]
        })


    @srcMLifyCode("tests/test_data/stereotype/factory.cpp")
    def test_factoryOne(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 1,
            "functionInfo":
            [
                ("clone", ['property', 'collaborator', 'factory', 'stateless'])
            ]
        })


    @srcMLifyCode("tests/test_data/stereotype/factory_2.cpp")
    def test_factoryTwo(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 1,
            "functionInfo":
            [
                ("clone", ['collaborator', 'factory', 'stateless'])
            ]
        })


    @srcMLifyCode("tests/test_data/xslt_functions/quantlib_fix.cpp")
    def test_quantlibFix(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 9,
            "functionInfo":
            [
                ("code", ["non-void-command","collaborator"]),
                ("date", ["non-void-command", "collaborator"]),
                ("nextDate", ["non-void-command", "collaborator"]),
                ("nextDate", ["non-void-command", "collaborator"]),
                ("nextCode", ["non-void-command", "collaborator"]),
                ("nextCode", ["non-void-command", "collaborator"]),
                ("testJuValues", ["command", "collaborator"]),
                ("testFdValues", ["command", "collaborator"]),
                ("suite", ["non-void-command","collaborator","factory"])
                
            ]
        })


    @srcMLifyCode("tests/test_data/to_fix_3.cpp")
    def test_toFixThree(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 8,
            "functionInfo":
            [
                ("checkWidth", ["unclassified"]),
                ("replaceColumn", ["unclassified"]),
                ("addColumn", ["unclassified"]),
                ("doubleArrayAt", ["unclassified"]),
                ("checkWidth", ['command', 'collaborator']),
                ("t_action",["get"]),
                ("checkForImage", ["collaborator"]),
                ("setLabelAt", ["command"]),
                
            ]
        })


    @srcMLifyCode("tests/test_data/to_fix_4.cpp")
    def test_toFixFour(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 19,
            "functionInfo":
            [
                ("t_action", ["get"]),
                ("t_action", ["get"]),
                ("FindVertex", ["get", "collaborator"]),
                ("checkForImage", ["collaborator"]),
                ("createNTupleToFile", ["non-void-command", "collaborator"]),
                ("registerNTuple", ["collaborator"]),
                ("setLabelAt", ["command"]),
                ("SetValue", ["unclassified"]),
                ("getTargetProjector", ["property","collaborator","factory"]),
                ("initPlot", ["command"]),
                ("drawLines", ["command", "collaborator"]),
                ("reset", ["command"]),
                ("run", ["collaborator"]),
                ("setFamily", ["unclassified"]),
                ("saveToFile", ['nonconstget', 'collaborator']),
                ("findWhite", ["nonconstget"]),
                ("findWhite", ["unclassified"]),
                ("endPlot", ["set"]),
                ("checkWidth", ["collaborator"]),
            ]
        })


    # 
    # @srcMLifyCode("tests/test_data/NTupleChiSqFCN.cpp")
    # def test_NTupleChiSqFCN(self, tree):
    #     quickDumpFunctionStereotypeInfo(tree, stereocodeDoc)



    # def test_Hippos(self):

    #     print "Processing Hippo Draw"

    #     # with memory_buffer() as buff:
    #     # with writable_archive(writable_archive_settings(default_language=language), filename="../hippodraw_archive.ann.xml") as archive_writer:
    #     #     u = archive_writer.create_unit()
    #     #     u.parse(filename=fileToProcess)
    #     #     archive_writer.write(u)
    #     print "Loading document"
    #     hippoDrawDoc = et.fromstringlist(open("/home/brian/Projects/srcTools/stereocode/hippodraw_archive.cpp.xml", "r"))
    #     print "loaded document"
    #     transformedHippoDocument = executeTransform(hippoDrawDoc, stereocodeDoc)
    #     print "Transformations applied"
    #     generateTestReport(transformedHippoDocument, "hippodrawReport")
    #     print "Report Generated"
    #     transformedHippoDocument.write("/home/brian/Projects/srcTools/stereocode/hippodraw_archive.cpp.ann.xml")
    #     print "Writing document"


    # def test_hippoDrawRefactorings(self):
    #     # generateStereotypeReportFromDoc

    #     print "Testing refactorings"
    #     currentHippoDrawDoc = et.fromstringlist(open("hippodraw_archive.cpp.xml", "r"))
    #     transformedHippoDocument = executeTransform(currentHippoDrawDoc, stereocodeDoc)


    #     expectedHippoDrawDoc = et.fromstringlist(open("previous_hippo_draw.xml", "r"))

    #     expectedResults = generateStereotypeReportFromDoc(expectedHippoDrawDoc)
    #     actualResults = generateStereotypeReportFromDoc(transformedHippoDocument)
    #     self.assertEqual(
    #         len(expectedResults),
    #         len(actualResults),
    #         "Incorrect # of results between actual and expected. Expected: {0} Actual: {1}".format(len(expectedResults), len(actualResults))
    #     )
    #     hasMismatchedStereotypes = False
    #     for dataToTest in zip(expectedResults, actualResults):
    #         if dataToTest[0][0] != dataToTest[1][0] or dataToTest[0][1] != dataToTest[1][1] or dataToTest[0][2] != dataToTest[1][2]:
    #             hasMismatchedStereotypes = True
    #             print """Expected:
    #             {0}
    #             {1}
    #             {2}

    #             Actual:
    #             {3}
    #             {4}
    #             {5}""".format(**dataToTest)

    #     self.assertFalse(hasMismatchedStereotypes, "Stereotype mismatched See Output")

