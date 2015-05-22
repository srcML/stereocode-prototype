##
# @file test_unique_histogram.py
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



class TestUniqueHistogramExtractor(unittest.TestCase):

    @gen_managed_file("test_unique_histogram_extractor.xml", """<?xml version="1.0" encoding="ISO-8859-1"?>
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
    def test_unique_histogram_extractor(self, filename):
        histogram = unique_histogram_extractor()
        run_info_extractor(filename, [histogram])
        self.assertEqual(1, histogram.histogram["collaborator command"], "Incorrect # from stereotype")
        self.assertEqual(2, histogram.histogram["unclassified"], "Incorrect # from stereotype")
        self.assertEqual(3, histogram.histogram["command"], "Incorrect # from stereotype")