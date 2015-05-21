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
        # run_info_extractor(filename, [])
