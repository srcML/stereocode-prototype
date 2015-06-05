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
from test_run_stereocode import *
from test_info_extractor import *
from test_histogram_extractor import *
from test_unique_histogram_extractor import *
from test_extract_funcion_list import *
from test_more_native_types import *
from test_more_modifiers import *
from test_known_namespaces import *
from test_ignorable_calls import *

from stereocode import *
from testlib import *
from srcml import *

if __name__ == '__main__':

    # Leave as false for now because it takes to long to run otherwise.
    if False:
        testTracker = CodeBaseTestDataTracker()
        testTracker.runTest(
            # inputFile,
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/ACE___5.6.1___ACEOnly___ACE_wrappers___annotated___all.ann.xml",
            [
                ("ACEXML_ENV_ARG_DECL_NOT_USED", "src:macro"),
                ("ACE_ALLOC_HOOK_DEFINE","src:macro"),
                ("ACE_END_VERSIONED_NAMESPACE_DECL", "src:macro"),
                ("ACE_BEGIN_VERSIONED_NAMESPACE_DECL", "src:macro"),
                ("ACE_RCSID", "src:macro"),
                ("ACE_TSS_TYPE", "src:type")
            ],
            10022,
            2771
        )

        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/ACE___ACE___annotated___all.ann.xml",
            [
                ("ACEXML_ENV_ARG_DECL_NOT_USED", "src:macro"),
                ("ACE_ALLOC_HOOK_DEFINE","src:macro"),
                ("ACE_END_VERSIONED_NAMESPACE_DECL", "src:macro"),
                ("ACE_BEGIN_VERSIONED_NAMESPACE_DECL", "src:macro"),
                ("ACE_RCSID", "src:macro"),
                ("ACE_STATIC_SVC_DEFINE", "src:macro"),
                ("ACE_PREALLOCATE_OBJECT", "src:macro"),
                ("ACE_PREALLOCATE_ARRAY", "src:macro"),
                ("ACE_DELETE_PREALLOCATED_ARRAY", "src:macro"),
                ("ACE_DELETE_PREALLOCATED_OBJECT", "src:macro"),
                ("ACE_APPLICATION_PREALLOCATED_OBJECT_DEFINITIONS", "src:macro"),
                ("ACE_APPLICATION_PREALLOCATED_ARRAY_DEFINITIONS", "src:macro"),
                ("ACE_TSS_TYPE", "src:type")
            ],
            10184,
            2882
        )

        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/ATM___annotated___all.ann.xml",
            [
            ],
            84,
            16
        )

        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/CEL___cel-src-1.2.1___annotated___all.ann.xml",
            [
                ("CEL_IMPLEMENT_FACTORY_ALT", "src:macro"),
                ("CS_IMPLEMENT_PLUGIN", "src:macro")
            ],
            2984,
            360
        )

        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/C++Fuzzy___Source___annotated___all.ann.xml",
            [
            ],
            313,
            29
        )


        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/CGAL___CGAL-3.4___annotated___all.ann.xml",
            [
                ("CGAL_BEGIN_NAMESPACE", "src:macro"),
                ("CGAL_END_NAMESPACE", "src:macro"),
                ("CGAL_double", "src:macro"),
                ("CGAL_int", "src:macro")

            ],
            26462,
            2933
        )


        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/ClanLib___0.8.0___annotated___all.ann.xml",
            [

            ],
            4650,
            1117
        )

        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/ClanLib___ClanLib-0.8.1___annotated___all.ann.xml",
            [

            ],
            4775,
            1137
        )

        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/CodeBlocks___codeblocks-8.02___annotated___all.ann.xml",
            [
                ("WX_PG_IMPLEMENT_EDITOR_CLASS", "src:macro"),
                ("WX_PG_DECLARE_ATTRIBUTE_METHODS", "src:macro"),
                ("WX_PG_DECLARE_ATTRIBUTE_METHODS", "src:macro"),
                ("WX_PG_DECLARE_BASIC_TYPE_METHODS", "src:macro"),
                ("WX_PG_IMPLEMENT_PROPERTY_CLASS", "src:macro"),
                ("wxPG_END_PROPERTY_CLASS_BODY", "src:macro"),
                ("WX_PG_IMPLEMENT_DERIVED_PROPERTY_CLASS", "src:macro"),
                ("WX_PG_DECLARE_VALIDATOR_METHODS", "src:macro"),
                ("WX_PG_DECLARE_ATTRIBUTE_METHODS", "src:macro"),
                ("wxT", "src:macro"),
                ("wxPG_UINT_TEMPLATE_MAX", "src:macro"),
                ("WXUNUSED", "src:macro"),
                ("DECLARE_EVENT_TABLE", "src:macro"),
                ("BEGIN_EVENT_TABLE", "src:macro"),
                ("EVT_SET_FOCUS", "src:macro"),
                ("EVT_KILL_FOCUS", "src:macro"),
                ("EVT_KEY_DOWN", "src:macro"),
                ("EVT_CHAR", "src:macro"),
                ("END_EVENT_TABLE", "src:macro"),
                ("EVT_LIST_ITEM_ACTIVATED", "src:macro"),
                ("EVT_SIZE", "src:macro"),
            ],
            12243,
            1377
        )


        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/CppUnit2___1.10.2___annotated___all.ann.xml",
            [
            ],
            1329,
            353
        )

        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/CppUnit2___cppunit-1.12.1___annotated___all.ann.xml",
            [
                ("CPPUNIT_NS_BEGIN", "src:macro"),
                ("CPPUNIT_NS_END", "src:macro")
            ],
            1360,
            357
        )
        
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/FlightGearNatalia___FlightGear-1.9.1___annotated___all.ann.xml",
            [],
            6102,
            876
        )

        
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/GScript___ghostscript-8.54___annotated___all.ann.xml",
            [],
            65,
            647
        )

        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/Ice___Ice-3.3.0___annotated___all.ann.xml",
            [],
            7533,
            1173
        )

        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/ICU___icu-4_0_1___annotated___all.ann.xml",
            [
                ("UOBJECT_DEFINE_RTTI_IMPLEMENTATION", "src:macro"),
                ("U_NAMESPACE_BEGIN", "src:macro"),
                ("U_NAMESPACE_END", "src:macro"),
                ("UOBJECT_DEFINE_RTTI_IMPLEMENTATION","src:macro"),
                ("U_CDECL_BEGIN", "src:macro"),
                ("U_CDECL_END", "src:macro"),
                ("UOBJECT_DEFINE_RTTI_IMPLEMENTATION", "src:macro")

            ],
            6214,
            1125
        )

        # 
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/Ivf++___ivf-depend-source-win32-msvc-8___annotated___all.ann.xml",
            [],
            2041,
            643
        )

        
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/Ivf++___ivfplusplus___ivf-1.0.0___annotated___all.ann.xml",
            [],
            3042,
            508
        )

        # 
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/libkate___annotated___all.ann.xml",
            [],
            1972,
            111
        )

        
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/MySQL++___mysql++-2.3.2___annotated___all.ann.xml",
            [],
            379,
            84
        )

        # 
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/PPTactical___PPTactical_Engine_0.9.6___annotated___all.ann.xml",
            [
                ("__fastcall", "src:specifier")
            ],
            5044,
            879
        )

        
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/Qt___4.1.2___qt-win-opensource-src-4.1.2___src___annotated___all.ann.xml",
            [
                ("QT_BEGIN_NAMESPACE", "src:macro"),
                ("QT_END_NAMESPACE", "src:macro"),
                ("Q_GLOBAL_STATIC", "src:macro"),
                ("Q_PROPERTY", "src:macro"),
                ("Q_OBJECT", "src:macro"),
                ("Q_CLASSINFO", "src:macro"),
                ("Q_GLOBAL_STATIC_WITH_ARGS", "src:macro"),
                ("QT_USE_NAMESPACE", "src:macro"),
                ("QT_BEGIN_INCLUDE_NAMESPACE", "src:macro"),
                ("QT_END_INCLUDE_NAMESPACE", "src:macro"),
                ("QML_INSTR_HEADER", "src:macro"),
                ("FT_BEGIN_HEADER", "src:macro"),
                ("HB_BEGIN_HEADER", "src:macro"),
                ("Q_CHECK_PAINTEVENTS", "src:macro"),
                ("QTEST_DISABLE_KEYPAD_NAVIGATION", "src:macro"),
                ("Q_DUMMY_ACCESSOR", "src:macro"),
                ("QML_GETTYPENAMES", "src:macro"),
                ("BEGIN_OPCODE", "src:case"),
                ("Q_DECLARE_SHARED", "src:macro"),
                ("Q_DECLARE_OPERATORS_FOR_FLAGS", "src:macro"),
                ("STACK_OF", "src:name"),
                ("Q_OUTOFLINE_TEMPLATE", "src:specifier"),
                ("Q_CORE_EXPORT","src:specifier"),
                ("Q_INLINE_TEMPLATE","src:specifier"),
                ("QT3_SUPPORT_CONSTRUCTOR","src:macro"),
                # ("STDMETHODIMP","src:name"),
                ("STDMETHODIMP_","src:macro")

            ],
            17126,
            1292
        )

        
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/Qt___4.3.3___tools___designer___src___components___formeditor___annotated___all.ann.xml",
            [
                ("QT_BEGIN_NAMESPACE", "src:macro"),
                ("QT_END_NAMESPACE", "src:macro"),
                ("Q_GLOBAL_STATIC", "src:macro"),
                ("Q_PROPERTY", "src:macro"),
                ("Q_OBJECT", "src:macro"),
                ("Q_CLASSINFO", "src:macro"),
                ("Q_GLOBAL_STATIC_WITH_ARGS", "src:macro"),
                ("QT_USE_NAMESPACE", "src:macro"),
                ("QT_BEGIN_INCLUDE_NAMESPACE", "src:macro"),
                ("QT_END_INCLUDE_NAMESPACE", "src:macro"),
                ("QML_INSTR_HEADER", "src:macro"),
                ("FT_BEGIN_HEADER", "src:macro"),
                ("HB_BEGIN_HEADER", "src:macro"),
                ("Q_CHECK_PAINTEVENTS", "src:macro"),
                ("QTEST_DISABLE_KEYPAD_NAVIGATION", "src:macro"),
                ("Q_DUMMY_ACCESSOR", "src:macro"),
                ("QML_GETTYPENAMES", "src:macro"),
                ("BEGIN_OPCODE", "src:case"),
                ("Q_DECLARE_SHARED", "src:macro"),
                ("Q_DECLARE_OPERATORS_FOR_FLAGS", "src:macro"),
                ("STACK_OF", "src:name"),
                ("Q_OUTOFLINE_TEMPLATE", "src:specifier"),
                ("Q_CORE_EXPORT","src:specifier"),
                ("Q_INLINE_TEMPLATE","src:specifier"),
                ("QT3_SUPPORT_CONSTRUCTOR","src:macro"),
                ("STDMETHODIMP_","src:macro")
            ],
            416,
            48
        )

        
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/QuantLib___QuantLib-0.9.7___annotated___all.ann.xml",
            [],
            5584,
            1694
        )

        # 
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/QuantLib___QuantLib___annotated___all.ann.xml",
            [],
            408,
            112
        )


        # 
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/Test___last_fix___annotated___all.ann.xml",
            [],
            5,
            6
        )

        # 
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/Test___last_fix___DataSource___annotated___all.ann.xml",
            [],
            4,
            4
        )

        # 
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/Test___last_fix___QDataStream___annotated___all.ann.xml",
            [],
            1,
            2
        )

        # 
        testTracker.runTest(
            "/home/brian/Projects/srcTools/stereocode/archive_test_data/Test___t1___annotated___all.ann.xml",
            [],
            94,
            1
        )

    unittest.main()
