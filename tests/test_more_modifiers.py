##
# @file test_more_modifiers.py
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


import unittest, lxml.etree as et, lxml, os, os.path, cStringIO
from stereocode import *
from testlib import *


class TestMoreModifiers(unittest.TestCase):
    @srcMLifyCode("tests/test_data/xslt_parameters/modifiers.cpp")
    @gen_managed_file("test_more_modifiers.txt", """
        AN_INLINING_MACRO
        """)
    def test_more_modifiers(self, filename, tree):
        # print "DERP!"
        output_stream = cStringIO.StringIO(et.tostring(tree))
        temp = output_stream.getvalue()
        # print temp
        cfg = configuration(
            mode=MODE_ADD_XML_ATTR,
            input_from=cStringIO.StringIO(temp),
            output_to=cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = cStringIO.StringIO(),
            unique_histogram_stream = None,
            no_redocumentation = False,
            ns_prefix_stream = None,
            more_modifiers_stream=open(filename, "r"),
            remove_redoc = False,
            extract_func_list=None
        )
        run_stereocode(cfg)
        temp = cfg.output_stream.getvalue()
        # print temp
        transformed_doc = et.XML(temp)
        located_stereotypes = transformed_doc.xpath("//src:function/@stereotype", namespaces=xmlNamespaces)
        self.assertEqual(
            1,
            len(located_stereotypes),
            "Didn't locate correct # of namespaces within document. Located #: {0}\n\nLocated Stereotypes: \n{1}".format(
                len(located_stereotypes),
                "\n".join([elem for elem in located_stereotypes])
            )
        )
        self.assertEqual("empty", str(located_stereotypes[0]).strip(), "Incorrect stereotypes. Expected: {0} Actual: {1}".format("collaborator", located_stereotypes[0]))