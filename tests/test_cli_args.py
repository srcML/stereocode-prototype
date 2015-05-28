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

        self.assertFalse(result.output_histogram, "Didn't get expected value.")
        self.assertIsNone(result.histogram_stream, "Didn't get expected value.")

        self.assertFalse(result.output_unique_histogram, "Didn't get expected value.")
        self.assertIsNone(result.unique_histogram_stream, "Didn't get expected value.")

        self.assertFalse(result.has_ns_pefix_file, "Didn't get expected values")
        self.assertIsNone(result.ns_pefix_file_stream, "Didn't get expected value.")

        self.assertFalse(result.no_redoc, "Didn't get expected value.")
        self.assertFalse(result.remove_redoc, "Didn't get expected value.")
        

    # testing input file.
    def test_input_from_console(self):
        config = parse_cli_arguments("", False)
        self.assertEqual(config.input_stream.__class__, sys.stdin.__class__, "Didn't get correct object for input")

    @cleanup_files("xmlTestFile.xml")
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

    def test_remove_redocumentation(self):
        config = parse_cli_arguments("--remove-redoc", False)
        self.assertTrue(config.remove_redoc, "Didn't correctly set remove redocumentation value")


    # Testing mode
    def test_mode_ReDocSrc(self):
        config = parse_cli_arguments("-m ReDocSrc", False)
        self.assertEqual(config.mode, MODE_REDOCUMENT_SOURCE, "Didn't correctly set mode")

    def test_mode_attrRedoc(self):
        config = parse_cli_arguments("-m XmlAttr", False)
        self.assertEqual(config.mode, MODE_ADD_XML_ATTR, "Didn't correctly set mode")

    @cleanup_files("FuncList.txt")
    def test_extract_function_list(self):
        config = parse_cli_arguments("-f FuncList.txt", False)
        # self.assertEqual(config.mode, MODE_FUNCTION_LIST, "Didn't correctly set mode")
        self.assertTrue(config.function_list_stream)

    # testing verbose
    def test_verbose(self):
        config = parse_cli_arguments("-v", False)
        self.assertTrue(config.verbose_output, "Didn't correctly set verbose")

    # Testing timings
    def test_timings(self):
        config = parse_cli_arguments("-t", False)
        self.assertTrue(config.output_timings, "Didn't correctly set timings")

    # No redocumentation testing
    @cleanup_files("no_redoc_temp.txt")
    def test_no_redoc(self):
        no_redoc_temp ="no_redoc_temp.txt"
        strm = open(no_redoc_temp, "w")
        strm.close()
        config = parse_cli_arguments("-n --histogram no_redoc_temp.txt", False)
        self.assertTrue(config.no_redoc, "Didn't correctly set no_redoc")


    # Testing histogram
    @cleanup_files("h_temp.txt")
    def test_histogram(self):
        config = parse_cli_arguments("--histogram h_temp.txt", False)
        self.assertTrue(config.output_histogram, "Didn't correctly set histogram")
        self.assertEqual(config.histogram_stream.__class__, file, "Didn't get correct object type for input. Actual: {0} Expected: {1}".format(config.histogram_stream.__class__.__name__, file))

    # Testing unique histogram
    @cleanup_files("uh_temp.txt")
    def test_unique_histogram(self):
        config = parse_cli_arguments("--unique-histogram uh_temp.txt", False)
        self.assertTrue(config.output_unique_histogram, "Didn't correctly set unique histogram")
        self.assertEqual(config.unique_histogram_stream.__class__, file, "Didn't get correct object type for input. Actual: {0} Expected: {1}".format(config.unique_histogram_stream.__class__.__name__, file))

    # Testing namespace file name
    @cleanup_files("ns_file.txt")
    def test_namespace(self):
        ns_file = "ns_file.txt"
        temp = open(ns_file, "w")
        temp.close()
        config = parse_cli_arguments("--ns-file ns_file.txt", False)
        self.assertTrue(config.has_ns_pefix_file, "Didn't correctly open file.")
        self.assertEqual(config.ns_pefix_file_stream.__class__, file, "Didn't get correct object type for input. Actual: {0} Expected: {1}".format(config.ns_pefix_file_stream.__class__.__name__, file))

    @expect_exception(cli_error)
    def test_namespace_missing_file(self):
        config = parse_cli_arguments("--ns-file does_not_exist.txt", False)


    @expect_exception(cli_error)
    def test_no_redoc_remove_redoc(self):
        config = parse_cli_arguments("--no-redoc --remove-redoc", False)

    @expect_exception(cli_error)
    def test_ns_file_remove_redoc(self):
        config = parse_cli_arguments("--ns-file ns_list.txt --remove-redoc", False)

    @expect_exception(cli_error)
    def test_no_redoc_nothing_to_be_done(self):
        config = parse_cli_arguments("--no-redoc", False)