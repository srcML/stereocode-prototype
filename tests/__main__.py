##
# @file __main__.py
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

import unittest, sys, lxml.etree as et, lxml, os, os.path
from test_cli_args import *
from test_stereotype_xslt import *
from stereocode import *
from testlib import *
from srcml import *

if __name__ == '__main__':

    # print 80 * "-"
    # print "Testing against previous stereotypes"
    # print 80 * "-"
    # Handling special test cases that are run after the initial test suite so that they can
    # test a larger mount of projects.

    # Walking all of the directories and re-srcml-ing
    # each of the files from within an all archive, then
    # re-running stereocode on it and testing the result
    # to see if the stereotypes are the same or different.
    # testTracker = CodeBaseTestDataTracker()
    # inputFile = "/home/brian/Projects/srcTools/stereocode/archive_test_data/reports/Code/actual__CDR_Stream_0_possibleBug.cpp.xml"
    # testTracker.runTest(
    #     # inputFile,
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/ACE___5.6.1___ACEOnly___ACE_wrappers___annotated___all.ann.xml",
    #     [
    #         ("ACEXML_ENV_ARG_DECL_NOT_USED", "src:macro"),
    #         ("ACE_ALLOC_HOOK_DEFINE","src:macro"),
    #         ("ACE_END_VERSIONED_NAMESPACE_DECL", "src:macro"),
    #         ("ACE_BEGIN_VERSIONED_NAMESPACE_DECL", "src:macro"),
    #         ("ACE_RCSID", "src:macro"),
    #         ("ACE_TSS_TYPE", "src:type")
    #     ],
    #     1000,
    #     1700
    # )

    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/ACE___ACE___annotated___all.ann.xml",
    #     [
    #         ("ACEXML_ENV_ARG_DECL_NOT_USED", "src:macro"),
    #         ("ACE_ALLOC_HOOK_DEFINE","src:macro"),
    #         ("ACE_END_VERSIONED_NAMESPACE_DECL", "src:macro"),
    #         ("ACE_BEGIN_VERSIONED_NAMESPACE_DECL", "src:macro"),
    #         ("ACE_RCSID", "src:macro"),
    #         ("ACE_STATIC_SVC_DEFINE", "src:macro"),
    #         ("ACE_PREALLOCATE_OBJECT", "src:macro"),
    #         ("ACE_PREALLOCATE_ARRAY", "src:macro"),
    #         ("ACE_DELETE_PREALLOCATED_ARRAY", "src:macro"),
    #         ("ACE_DELETE_PREALLOCATED_OBJECT", "src:macro"),
    #         ("ACE_APPLICATION_PREALLOCATED_OBJECT_DEFINITIONS", "src:macro"),
    #         ("ACE_APPLICATION_PREALLOCATED_ARRAY_DEFINITIONS", "src:macro"),
    #         ("ACE_TSS_TYPE", "src:type")
    #     ],
    #     10178,
    #     2882
    # )

    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/ATM___annotated___all.ann.xml",
    #     [
    #     ],
    #       1000,
    #     1700
    #)

    #testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/CEL___cel-src-1.2.1___annotated___all.ann.xml",
    #     [
    #         ("CEL_IMPLEMENT_FACTORY_ALT", "src:macro"),
    #         ("CS_IMPLEMENT_PLUGIN", "src:macro")
    #     ],
    #     10000,
    #     360
    # )

    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/C++Fuzzy___Source___annotated___all.ann.xml",
    #     [
    #         # ("CEL_IMPLEMENT_FACTORY_ALT", "src:macro"),
    #     ],
    #     10000,
    #     360
    # )


    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/CGAL___CGAL-3.4___annotated___all.ann.xml",
    #     [
    #         ("CGAL_BEGIN_NAMESPACE", "src:macro"),
    #         ("CGAL_END_NAMESPACE", "src:macro"),
    #         ("CGAL_double", "src:macro"),
    #         ("CGAL_int", "src:macro")

    #     ],
    #     10000,
    #     2933
    # )


    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/ClanLib___0.8.0___annotated___all.ann.xml",
    #     [

    #     ],
    #     10000,
    #     2933
    # )

    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/ClanLib___ClanLib-0.8.1___annotated___all.ann.xml",
    #     [

    #     ],
    #     10000,
    #     1137
    # )

    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/CodeBlocks___codeblocks-8.02___annotated___all.ann.xml",
    #     [
    #         ("WX_PG_IMPLEMENT_EDITOR_CLASS", "src:macro"),
    #         ("WX_PG_DECLARE_ATTRIBUTE_METHODS", "src:macro"),
    #         ("WX_PG_DECLARE_ATTRIBUTE_METHODS", "src:macro"),
    #         ("WX_PG_DECLARE_BASIC_TYPE_METHODS", "src:macro"),
    #         ("WX_PG_IMPLEMENT_PROPERTY_CLASS", "src:macro"),
    #         ("wxPG_END_PROPERTY_CLASS_BODY", "src:macro"),
    #         ("WX_PG_IMPLEMENT_DERIVED_PROPERTY_CLASS", "src:macro"),
    #         ("WX_PG_DECLARE_VALIDATOR_METHODS", "src:macro"),
    #         ("WX_PG_DECLARE_ATTRIBUTE_METHODS", "src:macro"),
    #         ("wxT", "src:macro"),
    #         ("wxPG_UINT_TEMPLATE_MAX", "src:macro"),
    #         ("WXUNUSED", "src:macro"),
    #         ("DECLARE_EVENT_TABLE", "src:macro"),
    #         ("BEGIN_EVENT_TABLE", "src:macro"),
    #         ("EVT_SET_FOCUS", "src:macro"),
    #         ("EVT_KILL_FOCUS", "src:macro"),
    #         ("EVT_KEY_DOWN", "src:macro"),
    #         ("EVT_CHAR", "src:macro"),
    #         ("END_EVENT_TABLE", "src:macro"),
    #         ("EVT_LIST_ITEM_ACTIVATED", "src:macro"),
    #         ("EVT_SIZE", "src:macro"),
    #     ],
    #     10859,
    #     1378
    # )


    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/CppUnit2___1.10.2___annotated___all.ann.xml",
    #     [
    #     ],
    #     10000,
    #     1378
    # )

    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/CppUnit2___cppunit-1.12.1___annotated___all.ann.xml",
    #     [
    #         ("CPPUNIT_NS_BEGIN", "src:macro"),
    #         ("CPPUNIT_NS_END", "src:macro")
    #     ],
    #     10000,
    #     1378
    # )

    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/CrystalSpace___crystalspace-src-1.2___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/CrystalSpace-src-1.2__50Units.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # Has NASTY bug
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/Doxygen___doxygen-1.5.8___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378,
    #     None
    # )


    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/filezilla-3.0.0___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/FlightGearNatalia___FlightGear-1.9.1___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/GScript___ghostscript-8.54___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     647
    # )

    # TOO MANY BROKEN MACROS!!
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/HippoDraw___HippoDraw-1.21.2___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     692
    #     # ,OPTION_CPP_TEXT_ELSE
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/HippoDraw___HippoDraw-1.21.3___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/Ice___Ice-3.3.0___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1173
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/ICU___icu-4_0_1___annotated___all.ann.xml",
    #     [
    #         ("UOBJECT_DEFINE_RTTI_IMPLEMENTATION", "src:macro"),
    #         ("U_NAMESPACE_BEGIN", "src:macro"),
    #         ("U_NAMESPACE_END", "src:macro"),
    #         ("UOBJECT_DEFINE_RTTI_IMPLEMENTATION","src:macro"),
    #         ("U_CDECL_BEGIN", "src:macro"),
    #         ("U_CDECL_END", "src:macro"),
    #         ("UOBJECT_DEFINE_RTTI_IMPLEMENTATION", "src:macro")

    #     ],
    #     10000,
    #     1125
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/Ivf++___ivf-depend-source-win32-msvc-8___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     643
    # )

    # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/Ivf++___ivfplusplus___ivf-1.0.0___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     508
    # )

    # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/KDE___KDevelop___3.5.0___annotated___all.ann.xml",
    #     [
    #         ("ANTLR_USE_NAMESPACE", "src:macro")
    #     ],
    #     10000,
    #     1710
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/KDE___KDevelop___3.5.0___src___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/libkate___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/MySQL++___mysql++-2.3.2___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/OpenWBEM___openwbem-3.2.2___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/PPTactical___PPTactical_Engine_0.9.6___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/Qt___4.1.2___qt-win-opensource-src-4.1.2___src___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/Qt___4.3.3___tools___designer___src___components___formeditor___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/QuantLib___QuantLib-0.9.7___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/QuantLib___QuantLib___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/SmartWin++___SmartWin___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # #
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/Test09___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/Test___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/Test___last_fix___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/Test___last_fix___DataSource___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/Test___last_fix___QDataStream___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/Test___t1___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/wxWidgets___2.8.6___src___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )

    # # 
    # testTracker.runTest(
    #     "/home/brian/Projects/srcTools/stereocode/archive_test_data/wxWidgets___2.8.6___src___mac___classic___annotated___all.ann.xml",
    #     [],
    #     10000,
    #     1378
    # )


    # filesToProcess = [f for f in os.listdir("archive_test_data") if os.path.isfile(os.path.join("archive_test_data", f))]
    # root = "archive_test_data"
    # for name in filesToProcess:
    #     currentName = os.path.join(root, name)
    #     # print "Processing: ", currentName
    #     testTracker.runTest(currentName)
    #     # print currentName

    # Running other parts of the test suite.
    # sys.stdout.flush()
    unittest.main()
