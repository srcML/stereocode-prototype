##
# @file test_cli_args.py
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

import unittest, sys, os
from testlib import *
from stereocode import *

class TestCLIArgs(unittest.TestCase):
    def test_default_parsed_arguments(self):
        result = parse_cli_arguments("", False)

        self.assertEqual(result.input_stream, sys.stdin, "Didn't get expected type.")
        self.assertEqual(result.output_stream, sys.stdout, "Didn't get expected type.")
        self.assertEqual(result.mode,processingModes[0], "Didn't get expected value.")
        self.assertFalse(result.verbose_output, "Didn't get expected value.")
        self.assertFalse(result.output_timings, "Didn't get expected value.")

    # def test_help(self):
    #     result = parse_cli_arguments("-h")
        # print 
        # self.assertTrue(isinstance(result.input, list), "Didn't get expected type.")
        # self.assertEqual(result.output, None, "Didn't get expected type.")
        # self.assertEqual(result.mode,processingModes[0], "Didn't get expected type.")
        # self.assertFalse(result.debug, "Didn't get expected type.")
        # self.assertFalse(result.enableTiming, "Didn't get expected type.")

    def test_input(self):
        config = parse_cli_arguments("", False)
        self.assertEqual(config.input_stream.__class__, sys.stdin.__class__, "Didn't get correct object for input")

    def test_input_from_file(self):
        outputFileName = "xmlTestFile.xml"
        xmlFileContent = """<?xml version="1.0" encoding="UTF-8"?>
<unit></unit>"""
        temp = open(outputFileName, "w")
        temp.write(xmlFileContent)
        temp.close()
        config = parse_cli_arguments("-i " + outputFileName, False)
        self.assertEqual(config.input_stream.__class__, file, "Didn't get correct object type for input. Actual: {0} Expected: {1}".format(config.input_stream.__class__.__name__, file))

    @expect_exception(cli_error)
    def test_from_invalid_file(self):
        config = parse_cli_arguments("-i something.xml", False)

    @expect_exception(cli_error)
    def test_remove_redocumentation_from_function_list(self):
        config = parse_cli_arguments("--remove-redoc -m FuncList", False)


    def test_remove_redocumentation(self):
        config = parse_cli_arguments("--remove-redoc", False)
        self.assertTrue(config.remove_redoc, "Didn't correctly set remove redocumentation value")


    def test_mode_ReDocSrc(self):
        config = parse_cli_arguments("-m ReDocSrc", False)
        self.assertEqual(config.mode, MODE_REDOCUMENT_SOURCE, "Didn't correctly mode")

    def test_mode_attrRedoc(self):
        config = parse_cli_arguments("-m XmlAttr", False)
        self.assertEqual(config.mode, MODE_ADD_XML_ATTR, "Didn't correctly mode")

    def test_mode_FuncList(self):
        config = parse_cli_arguments("-m FuncList", False)
        self.assertEqual(config.mode, MODE_FUNCTION_LIST, "Didn't correctly mode")
