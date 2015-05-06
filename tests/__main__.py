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

if __name__ == '__main__':

    print 80 * "-"
    print "Testing against previous stereotypes"
    print 80 * "-"
    # Handling special test cases that are run after the initial test suite so that they can
    # test a larger mount of projects.

    # Walking all of the directories and re-srcml-ing
    # each of the files from within an all archive, then
    # re-running stereocode on it and testing the result
    # to see if the stereotypes are the same or different.
    testTracker = CodeBaseTestDataTracker()
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
    #     ]
    #       1000,
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
    #     ]
    #     1000,
    #     1700
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


    testTracker.runTest(
        "/home/brian/Projects/srcTools/stereocode/archive_test_data/CGAL___CGAL-3.4___annotated___all.ann.xml",
        [
            ("CGAL_BEGIN_NAMESPACE", "src:macro"),
            ("CGAL_END_NAMESPACE", "src:macro"),
            ("CGAL_double", "src:macro"),
            ("CGAL_int", "src:macro")

        ],
        10000,
        360
    )

    # 

    # filesToProcess = [f for f in os.listdir("archive_test_data") if os.path.isfile(os.path.join("archive_test_data", f))]
    # root = "archive_test_data"
    # for name in filesToProcess:
    #     currentName = os.path.join(root, name)
    #     # print "Processing: ", currentName
    #     testTracker.runTest(currentName)
    #     # print currentName

    # Running other parts of the test suite.
    sys.stdout.flush()
    # unittest.main()
