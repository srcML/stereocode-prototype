##
# @file test_function_list_extractor.py
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
from libstereocode import *
from testlib import *



class TestExtractFunctionList(unittest.TestCase):


    @gen_managed_file("test_histogram_extractor.xml", """<?xml version="1.0" encoding="ISO-8859-1"?>
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
    def test_function_list_extractor(self, filename):
        extractor = function_list_extractor()
        run_info_extractor(filename, [extractor])
        # print "\n".join([str(x)for x in  extractor.func_info])
        """
{'functions': [

],
'archive_line_number': 4, 'filename': u'advgeom.cpp'}
        """
        self.assertEqual(1, len(extractor.functions_by_unit), "Incorrect # of units located")
        self.assertEqual(6, len([f for u in extractor.functions_by_unit for f in u.functions]), "Incorrect # of functions located")
        self.assertEqual(4, extractor.functions_by_unit[0].archive_line_number, "Incorrect archive line number")
        self.assertEqual("advgeom.cpp", extractor.functions_by_unit[0].filename, "Incorrect filename")

        # Testing function names, sigs, etc...
        #   'file_line_number': 2
        # current_func = extractor.functions_by_unit[0].functions[0]
        test_data = [
            {'is_within_class': False, 'name': 'CExampleWindow::onInit', 'archive_line_number': 6, 'signature': 'void CExampleWindow::onInit(int width, int height)', 'class_name': '', 'stereotypes': ['command', 'collaborator'], 'file_line_number': 2}, 
            {'is_within_class': False, 'name': 'CExampleWindow::onResize', 'archive_line_number': 9, 'signature': 'void CExampleWindow::onResize(int width, int height)', 'class_name': '', 'stereotypes': ['unclassified'], 'file_line_number': 5}, 
            {'is_within_class': False, 'name': 'CExampleWindow::onRender', 'archive_line_number': 12, 'signature': 'void CExampleWindow::onRender()', 'class_name': '', 'stereotypes': ['unclassified'], 'file_line_number': 8}, 
            {'is_within_class': False, 'name': 'CExampleWindow::onMouseDown', 'archive_line_number': 15, 'signature': 'void CExampleWindow::onMouseDown(int x, int y)', 'class_name': '', 'stereotypes': ['command'], 'file_line_number': 11}, 
            {'is_within_class': False, 'name': 'CExampleWindow::onMouseMove', 'archive_line_number': 18, 'signature': 'void CExampleWindow::onMouseMove(int x, int y)', 'class_name': '', 'stereotypes': ['command'], 'file_line_number': 14}, 
            {'is_within_class': False, 'name': 'CExampleWindow::onMouseUp', 'archive_line_number': 21, 'signature': 'void CExampleWindow::onMouseUp(int x, int y)', 'class_name': '', 'stereotypes': ['command'], 'file_line_number': 17}
        ]
        for t in zip(extractor.functions_by_unit[0].functions, test_data):
            self.validated_correct_func(*t)


    def validated_correct_func(self, current_func, expected):
        self.assertEqual(
            expected["is_within_class"],
            current_func.is_within_class,
            "Incorrect is_within_class. Expected: {0} Actual: {1}".format(
                expected["is_within_class"],
                current_func.is_within_class
            )
        )
        self.assertEqual(
            expected["name"],
            current_func.name,
            "Incorrect name. Expected: {0} Actual: {1}".format(
                expected["name"],
                current_func.name
            )
        )
        self.assertEqual(
            expected["signature"],
            current_func.signature,
            "Incorrect signature. Expected: {0} Actual: {1}".format(
                expected["signature"],
                current_func.signature
            )
        )
        self.assertEqual(
            expected["class_name"],
            current_func.class_name,
            "Incorrect class name prefix. Expected: {0} Actual: {1}".format(
                expected["class_name"],
                current_func.class_name
            )
        )
        self.assertListEqual(
            expected["stereotypes"],
            current_func.stereotypes,
            "Incorrect stereotypes. Expected: {0} Actual: {1}".format(
                expected["stereotypes"],
                current_func.stereotypes
            )
        )
        self.assertEqual(
            expected["archive_line_number"],
            current_func.archive_line_number,
            "Incorrect line # in archive. Expected: {0} Actual: {1}".format(
                expected["archive_line_number"],
                current_func.archive_line_number
            )
        )
        self.assertEqual(
            expected["file_line_number"],
            current_func.file_line_number,
            "Incorrect line # in file. Expected: {0} Actual: {1}".format(
                expected["file_line_number"],
                current_func.file_line_number
            )
        )