##
# @file test_info_extractor.py
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

import unittest, lxml.etree as et, lxml, os, os.path
from stereocode import *
from testlib import *


class unit_visit_data:
    def __init__(self, unit_name, extra_tests=None):
        self.unit_name = unit_name
        self.extra_tests = extra_tests
    
        
class func_visit_data:
    def __init__(self, stereotypes, function_name, function_sig, extra_tests=None):
        self.stereotypes = stereotypes
        self.function_name = function_name
        self.function_sig = function_sig
        self.extra_tests = extra_tests


class visitation_extraction_tester(extractor_base):
    def __init__(self, instance, visit_state_check):
        super(visitation_extraction_tester, self).__init__()
        self.unittest = instance
        self.on_visit_validation = visit_state_check
        self.visit_index = 0

    def start_document(self):
        # print "Starting Document"
        pass

    def end_document(self):
        self.unittest.assertEqual(len(self.on_visit_validation), self.visit_index, "Didn't visit the expected # of units and functions. Expected: {0} Actual: {1}".format(len(self.on_visit_validation), self.visit_index))

    def on_function(self, stereotype_list, function_name, function_signature, document_locator, info):
        current_function_data = self.on_visit_validation[self.visit_index]
        self.unittest.assertIsInstance(current_function_data, func_visit_data, "Didn't get correct visit_data type when visiting function. Current Data: Stereotypes: {0} Function Name: {1} Function Signature: {2}".format(stereotype_list, function_name, function_signature))
        self.unittest.assertListEqual(stereotype_list, current_function_data.stereotypes, "Incorrect Stereotypes. Expected: {4} Actual: {3} Current Data: Stereotypes: {0} Function Name: {1} Function Signature: {2}".format(stereotype_list, function_name, function_signature, stereotype_list, current_function_data.stereotypes))
        self.unittest.assertEqual(function_name, current_function_data.function_name, "Incorrect function_name. Expected: {4} Actual: {3} Current Data: Stereotypes: {0} Function Name: {1} Function Signature: {2}".format(stereotype_list, function_name, function_signature, function_name, current_function_data.function_name))
        self.unittest.assertEqual(function_signature, current_function_data.function_sig, "Incorrect function_name. Expected: {4} Actual: {3} Current Data: Stereotypes: {0} Function Name: {1} Function Signature: {2}".format(stereotype_list, function_name, function_signature, function_signature, current_function_data.function_sig))
        if current_function_data.extra_tests != None:
            current_function_data.extra_tests(self.unittest, stereotype_list, function_name, function_signature, document_locator, info)
        self.visit_index += 1

    def on_unit(self, filename, document_locator, info):
        current_visit_data = self.on_visit_validation[self.visit_index]
        self.unittest.assertIsInstance(current_visit_data, unit_visit_data, "Didn't get correct visit_data type when visiting unit. Current Unit Name:{0}: ".format(filename))
        self.unittest.assertEqual(filename, current_visit_data.unit_name, "Incorrect unit_name. Expected: {0} Actual: {1}".format(current_visit_data.unit_name, filename))

        if current_visit_data.extra_tests != None:
            current_visit_data.extra_tests(self.unittest, filename, document_locator, info)
        self.visit_index += 1



class TestInfoExtractor(unittest.TestCase):

    def test_info_extractor__default_constructor(self):
        handler = info_extractor([])
        
        self.assertListEqual([], handler.extractors, "Mismatched values.")
        self.assertIsNone(handler.document_locator, "Incorrect value")
        self.assertIsNone(handler.current_unit_name, "Incorrect value")
        self.assertFalse(handler.is_archive, "Incorrect value")
        self.assertEqual(MODE_REDOCUMENT_SOURCE, handler.configuration_mode, "Incorrect value")
        self.assertListEqual([], handler.cls_ns_stack, "Mismatched values.")
        self.assertEqual(STATE_START, handler.state, "Incorrect value")


    def test_constructor(self):
        handler = info_extractor([1,2,3], MODE_ADD_XML_ATTR)
        self.assertListEqual([1,2,3], handler.extractors, "Mismatched values.")
        self.assertEqual(MODE_ADD_XML_ATTR, handler.configuration_mode, "Incorrect value")

    @expect_exception(extractor_error)
    @gen_managed_file("info_extractor_test_invalid_archive.xml", """<?xml version="1.0" encoding="UTF-8"?><AArdvark></AArdvark>""")
    def test_invalid_archive(self, filename):
        run_info_extractor(filename, [])




    @gen_managed_file("test_class_name_tracking.xml", """<?xml version="1.0" encoding="ISO-8859-1"?>
<unit xmlns="http://www.srcML.org/srcML/src" >

<unit language="C++" xmlns:cpp="http://www.srcML.org/srcML/cpp" filename="filename">
<class> <name>thingy1</name> <block></block></class>
<class> <name>thingy2</name> <block><class> <name>thingy3</name> <block></block></class></block></class>
<class> <name>thingy4</name> <block><class> <name>thingy5</name> <block></block></class></block></class>

</unit>
</unit>""")
    def test_class_name_tracking(self, filename):
        handler = info_extractor([],)
        parse(filename, handler)
        self.assertEqual(0, len(handler.cls_ns_stack), "didn't correctly clear stack.")



    @gen_managed_file("test_unit_visitation_tests.xml", """<?xml version="1.0" encoding="ISO-8859-1"?>
<unit xmlns="http://www.srcML.org/srcML/src" revision="0.8.0" options="CPPIF_CHECK">

<unit xmlns:cpp="http://www.srcML.org/srcML/cpp" revision="0.8.0" language="C++" filename="f1.cpp"></unit>
<unit xmlns:cpp="http://www.srcML.org/srcML/cpp" revision="0.8.0" language="C++" filename="f2.cpp"></unit>
<unit xmlns:cpp="http://www.srcML.org/srcML/cpp" revision="0.8.0" language="C++" filename="f3.cpp"></unit>
<unit xmlns:cpp="http://www.srcML.org/srcML/cpp" revision="0.8.0" language="C++" filename="f4.cpp"></unit>
<unit xmlns:cpp="http://www.srcML.org/srcML/cpp" revision="0.8.0" language="C++" filename="f5.cpp"></unit>

</unit>""")
    def test_unit_visitation_tests(self, filename):
        run_info_extractor(filename, [visitation_extraction_tester(self,
            [
                unit_visit_data("f1.cpp"),
                unit_visit_data("f2.cpp"),
                unit_visit_data("f3.cpp"),
                unit_visit_data("f4.cpp"),
                unit_visit_data("f5.cpp"),
            ]
        )])





    @gen_managed_file("test_single_file_archive_unit_visitation.xml", """<?xml version="1.0" encoding="ISO-8859-1"?>
        <unit xmlns="http://www.srcML.org/srcML/src" revision="0.8.0" options="CPPIF_CHECK" language="C++" filename="f1.cpp"></unit>""")
    def test_single_file_archive_unit_visitation(self, filename):
        run_info_extractor(filename, [visitation_extraction_tester(self,
            [
                unit_visit_data("f1.cpp")
            ]
        )])





    @gen_managed_file("test_single_function_visitation_tests.xml", """<?xml version="1.0" encoding="ISO-8859-1"?>
<unit xmlns="http://www.srcML.org/srcML/src" revision="0.8.0" options="CPPIF_CHECK">

<unit xmlns:cpp="http://www.srcML.org/srcML/cpp" revision="0.8.0" language="C++" filename="f1.cpp">
<comment type="block">/** @stereotype command collaborator */</comment>
<function><type><name>void</name></type> <name><name>CExampleWindow</name><operator>::</operator><name>onInit</name></name><parameter_list>(<parameter><decl><type><name>int</name></type> <name>width</name></decl></parameter>, <parameter><decl><type><name>int</name></type> <name>height</name></decl></parameter>)</parameter_list><block>{}</block></function>

</unit>
</unit>""")
    def test_single_function_visitation_tests(self, filename):
        run_info_extractor(filename, [visitation_extraction_tester(self,
            [
                unit_visit_data("f1.cpp"),
                func_visit_data(["command", "collaborator"], "CExampleWindow::onInit", "void CExampleWindow::onInit(int width, int height)")
            ]
        )])


    @gen_managed_file("test_function_visitation_tests.xml", """<?xml version="1.0" encoding="ISO-8859-1"?>
<unit xmlns="http://www.srcML.org/srcML/src" revision="0.8.0" options="CPPIF_CHECK">

<unit xmlns:cpp="http://www.srcML.org/srcML/cpp" revision="0.8.0" language="C++" filename="advgeom.cpp">
<comment type="block">/** @stereotype command collaborator */</comment>
<function><type><name>void</name></type> <name><name>CExampleWindow</name><operator>::</operator><name>onInit</name></name><parameter_list>(<parameter><decl><type><name>int</name></type> <name>width</name></decl></parameter>, <parameter><decl><type><name>int</name></type> <name>height</name></decl></parameter>)</parameter_list><block>{}</block></function>

<comment type="block">/** @stereotype unclassified */</comment>
<function><type><name>void</name></type> <name><name>CExampleWindow</name><operator>::</operator><name>onResize</name></name><parameter_list>(<parameter><decl><type><name>int</name></type> <name>width</name></decl></parameter>, <parameter><decl><type><name>int</name></type> <name>height</name></decl></parameter>)</parameter_list><block>{}</block></function>

<comment type="block">/** @stereotype unclassified */</comment>
<function><type><name>void</name></type> <name><name>CExampleWindow</name><operator>::</operator><name>onRender</name></name><parameter_list>()</parameter_list><block>{}</block></function>

<comment type="block">/** @stereotype command */</comment>
<function><type><name>void</name></type> <name><name>CExampleWindow</name><operator>::</operator><name>onMouseDown</name></name><parameter_list>(<parameter><decl><type><name>int</name></type> <name>x</name></decl></parameter>, <parameter><decl><type><name>int</name></type> <name>y</name></decl></parameter>)</parameter_list><block>{}</block></function>

<comment type="block">/** @stereotype command */</comment>
<function><type><name>void</name></type> <name><name>CExampleWindow</name><operator>::</operator><name>onMouseMove</name></name><parameter_list>(<parameter><decl><type><name>int</name></type> <name>x</name></decl></parameter>, <parameter><decl><type><name>int</name></type> <name>y</name></decl></parameter>)</parameter_list><block>{}</block></function>

<comment type="block">/** @stereotype command */</comment>
<function><type><name>void</name></type> <name><name>CExampleWindow</name><operator>::</operator><name>onMouseUp</name></name><parameter_list>(<parameter><decl><type><name>int</name></type> <name>x</name></decl></parameter>, <parameter><decl><type><name>int</name></type> <name>y</name></decl></parameter>)</parameter_list><block>{}</block></function>

</unit>
</unit>""")
    def test_function_visitation_tests(self, filename):
        run_info_extractor(filename, [visitation_extraction_tester(self,
            [
                unit_visit_data("advgeom.cpp"),
                func_visit_data(["command", "collaborator"], "CExampleWindow::onInit", "void CExampleWindow::onInit(int width, int height)"),
                func_visit_data(["unclassified"], "CExampleWindow::onResize", "void CExampleWindow::onResize(int width, int height)"),
                func_visit_data(["unclassified"], "CExampleWindow::onRender", "void CExampleWindow::onRender()"),
                func_visit_data(["command"], "CExampleWindow::onMouseDown", "void CExampleWindow::onMouseDown(int x, int y)"),
                func_visit_data(["command"], "CExampleWindow::onMouseMove", "void CExampleWindow::onMouseMove(int x, int y)"),
                func_visit_data(["command"], "CExampleWindow::onMouseUp", "void CExampleWindow::onMouseUp(int x, int y)")
            ]
        )])


    @gen_managed_file("test_function_visitation_with_attribute_annotations.xml", """<?xml version="1.0" encoding="ISO-8859-1"?>
<unit xmlns="http://www.srcML.org/srcML/src" revision="0.8.0" options="CPPIF_CHECK">

<unit xmlns:cpp="http://www.srcML.org/srcML/cpp" revision="0.8.0" language="C++" filename="advgeom.cpp">
<function stereotype="command collaborator"><type><name>void</name></type> <name><name>CExampleWindow</name><operator>::</operator><name>onInit</name></name><parameter_list>(<parameter><decl><type><name>int</name></type> <name>width</name></decl></parameter>, <parameter><decl><type><name>int</name></type> <name>height</name></decl></parameter>)</parameter_list><block>{}</block></function>

<function stereotype="unclassified"><type><name>void</name></type> <name><name>CExampleWindow</name><operator>::</operator><name>onResize</name></name><parameter_list>(<parameter><decl><type><name>int</name></type> <name>width</name></decl></parameter>, <parameter><decl><type><name>int</name></type> <name>height</name></decl></parameter>)</parameter_list><block>{}</block></function>


<function stereotype="unclassified"><type><name>void</name></type> <name><name>CExampleWindow</name><operator>::</operator><name>onRender</name></name><parameter_list>()</parameter_list><block>{}</block></function>

<function stereotype="command"><type><name>void</name></type> <name><name>CExampleWindow</name><operator>::</operator><name>onMouseDown</name></name><parameter_list>(<parameter><decl><type><name>int</name></type> <name>x</name></decl></parameter>, <parameter><decl><type><name>int</name></type> <name>y</name></decl></parameter>)</parameter_list><block>{}</block></function>

<function stereotype="command"><type><name>void</name></type> <name><name>CExampleWindow</name><operator>::</operator><name>onMouseMove</name></name><parameter_list>(<parameter><decl><type><name>int</name></type> <name>x</name></decl></parameter>, <parameter><decl><type><name>int</name></type> <name>y</name></decl></parameter>)</parameter_list><block>{}</block></function>

<function stereotype="command"><type><name>void</name></type> <name><name>CExampleWindow</name><operator>::</operator><name>onMouseUp</name></name><parameter_list>(<parameter><decl><type><name>int</name></type> <name>x</name></decl></parameter>, <parameter><decl><type><name>int</name></type> <name>y</name></decl></parameter>)</parameter_list><block>{}</block></function>

</unit>
</unit>""")
    def test_function_visitation_with_attribute_annotations(self, filename):
        run_info_extractor(filename, [visitation_extraction_tester(self,
            [
                unit_visit_data("advgeom.cpp"),
                func_visit_data(["command", "collaborator"], "CExampleWindow::onInit", "void CExampleWindow::onInit(int width, int height)"),
                func_visit_data(["unclassified"], "CExampleWindow::onResize", "void CExampleWindow::onResize(int width, int height)"),
                func_visit_data(["unclassified"], "CExampleWindow::onRender", "void CExampleWindow::onRender()"),
                func_visit_data(["command"], "CExampleWindow::onMouseDown", "void CExampleWindow::onMouseDown(int x, int y)"),
                func_visit_data(["command"], "CExampleWindow::onMouseMove", "void CExampleWindow::onMouseMove(int x, int y)"),
                func_visit_data(["command"], "CExampleWindow::onMouseUp", "void CExampleWindow::onMouseUp(int x, int y)")
            ]
        )])