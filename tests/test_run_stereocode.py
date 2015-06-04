##
# @file test_run_stereocode.py
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
from csv import DictReader


class TestRunStereocode(unittest.TestCase):

    def parse_extract_histogram(self, input_stream, expected_dict):
        # temp_list = dict()
        # input_stream.getvalue()
        actual_histogram_dict = {item[1].strip():int(item[0].strip()) for item in [l.strip().split(":") for l in input_stream][3:] }
        # print actual_histogram_dict
        self.assertDictEqual(actual_histogram_dict, expected_dict, "Mismatched expected and actual dictionary: Actual: {0} Expected: {1}".format(actual_histogram_dict, expected_dict))


    
    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    def test_remove_stereotype(self, tree):
        output_stream = cStringIO.StringIO()
        stereocodeDoc(tree).write(output_stream)

        cfg = configuration(
            mode=MODE_REDOCUMENT_SOURCE,
            input_from=cStringIO.StringIO(output_stream.getvalue()),
            output_to=cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = None,
            unique_histogram_stream = None,
            
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = False,
            extract_func_list=None
        )
        remove_stereotypes(cfg)
        transformed_archive_stream = cStringIO.StringIO(cfg.output_stream.getvalue())
        no_stereotype_archive = et.parse(transformed_archive_stream)
        transformed_archive_stream.close()
        located_stereotypes = no_stereotype_archive.xpath("//src:comment[contains(text(), '@stereotype')]", namespaces=xmlNamespaces)
        self.assertEqual(
            0,
            len(located_stereotypes),
            "Didn't locate correct # of namespaces within document. Located #: {0}\n\nLocated Stereotypes: \n{1}".format(
                len(located_stereotypes),
                "\n".join([et.tostring(elem) for elem in located_stereotypes])
            )
        )


    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    def test_run_stereocode_redocument(self, tree):
        output_stream = cStringIO.StringIO()
        output_stream.write(et.tostring(tree))

        cfg = configuration(
            mode=MODE_REDOCUMENT_SOURCE,
            input_from=cStringIO.StringIO(output_stream.getvalue()),
            output_to=cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = None,
            unique_histogram_stream = None,
            
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = False,
            extract_func_list=None
        )

        run_stereocode(cfg)

        transformed_doc = et.XML(cfg.output_stream.getvalue())
        located_stereotypes = transformed_doc.xpath("//src:comment[contains(text(), '@stereotype')]", namespaces=xmlNamespaces)
        self.assertEqual(
            2,
            len(located_stereotypes),
            "Didn't locate correct # of namespaces within document. Located #: {0}\n\nLocated Stereotypes: \n{1}".format(
                len(located_stereotypes),
                "\n".join([et.tostring(elem) for elem in located_stereotypes])
            )
        )

    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    def test_remove_stereotypes_configuration(self, tree):
        output_stream = cStringIO.StringIO()
        stereocodeDoc(tree).write(output_stream)

        cfg = configuration(
            mode=MODE_REDOCUMENT_SOURCE,
            input_from=cStringIO.StringIO(output_stream.getvalue()),
            output_to=cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = None,
            unique_histogram_stream = None,
            
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = True,
            extract_func_list=None
        )

        run_stereocode(cfg)

        transformed_doc = et.XML(cfg.output_stream.getvalue())
        located_stereotypes = transformed_doc.xpath("//src:comment[contains(text(), '@stereotype')]", namespaces=xmlNamespaces)
        self.assertEqual(
            0,
            len(located_stereotypes),
            "Didn't locate correct # of namespaces within document. Located #: {0}\n\nLocated Stereotypes: \n{1}".format(
                len(located_stereotypes),
                "\n".join([et.tostring(elem) for elem in located_stereotypes])
            )
        )


    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    def test_run_stereocode_redocument_histogram(self, tree):
        output_stream = cStringIO.StringIO()
        output_stream.write(et.tostring(tree))

        cfg = configuration(
            mode=MODE_REDOCUMENT_SOURCE,
            input_from=cStringIO.StringIO(output_stream.getvalue()),
            output_to=cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = cStringIO.StringIO(),
            unique_histogram_stream = None,
            
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = False,
            extract_func_list=None
        )

        run_stereocode(cfg)

        transformed_doc = et.XML(cfg.output_stream.getvalue())
        located_stereotypes = transformed_doc.xpath("//src:comment[contains(text(), '@stereotype')]", namespaces=xmlNamespaces)
        self.assertEqual(
            2,
            len(located_stereotypes),
            "Didn't locate correct # of namespaces within document. Located #: {0}\n\nLocated Stereotypes: \n{1}".format(
                len(located_stereotypes),
                "\n".join([et.tostring(elem) for elem in located_stereotypes])
            )
        )
        self.parse_extract_histogram(cStringIO.StringIO(cfg.histogram_stream.getvalue()), {'collaborator': 1, 'nonconstget': 1, 'get': 1})

    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    def test_run_stereocode_redocument_unique_histogram(self, tree):
        output_stream = cStringIO.StringIO()
        output_stream.write(et.tostring(tree))

        cfg = configuration(
            mode=MODE_REDOCUMENT_SOURCE,
            input_from=cStringIO.StringIO(output_stream.getvalue()),
            output_to=cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = None,
            unique_histogram_stream = cStringIO.StringIO(),
            
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = False,
            extract_func_list=None
        )

        run_stereocode(cfg)

        transformed_doc = et.XML(cfg.output_stream.getvalue())
        located_stereotypes = transformed_doc.xpath("//src:comment[contains(text(), '@stereotype')]", namespaces=xmlNamespaces)
        self.assertEqual(
            2,
            len(located_stereotypes),
            "Didn't locate correct # of namespaces within document. Located #: {0}\n\nLocated Stereotypes: \n{1}".format(
                len(located_stereotypes),
                "\n".join([et.tostring(elem) for elem in located_stereotypes])
            )
        )
        self.parse_extract_histogram(cStringIO.StringIO(cfg.unique_histogram_stream.getvalue()), {'collaborator get': 1, 'nonconstget': 1})



    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    def test_run_stereocode_redocument_funclist(self, tree):
        output_stream = cStringIO.StringIO()
        output_stream.write(et.tostring(tree))
        # print >>sys.stderr, output_stream.getvalue()
        cfg = configuration(
            mode=MODE_REDOCUMENT_SOURCE,
            input_from=cStringIO.StringIO(output_stream.getvalue()),
            output_to=cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = None,
            unique_histogram_stream = None,
            
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = False,
            extract_func_list=cStringIO.StringIO()
        )

        run_stereocode(cfg)

        transformed_doc = et.XML(cfg.output_stream.getvalue())
        located_stereotypes = transformed_doc.xpath("//src:comment[contains(text(), '@stereotype')]", namespaces=xmlNamespaces)
        self.assertEqual(
            2,
            len(located_stereotypes),
            "Didn't locate correct # of namespaces within document. Located #: {0}\n\nLocated Stereotypes: \n{1}".format(
                len(located_stereotypes),
                "\n".join([et.tostring(elem) for elem in located_stereotypes])
            )
        )
        tempstr = cfg.function_list_stream.getvalue()
        # print tempstr
        csv_strm = cStringIO.StringIO(tempstr)
        csv_reader = DictReader(csv_strm)
        written_data=[
            ["y::match1","obj* y::match1() const","get,collaborator","tests/test_data/stereotype/get.cpp","12","9",""],
            ["y::match2","int y::match2()","nonconstget","tests/test_data/stereotype/get.cpp","17","14",""]
        ]
        index = 0
        for r in csv_reader:
            expected = dict(zip(csv_reader.fieldnames, written_data[index]))
            self.assertDictEqual(
                expected,
                r,
                "Incorrect output. Expected: {1} Actual:{0}".format(
                    "".join(["{0}: {1}\n".format(*x) for x in r.items()]),
                    "".join(["{0}: {1}\n".format(*x) for x in expected.items()])
                )
            )
            index += 1


    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    def test_run_stereocode_remove_redocument_histogram(self, tree):
        output_stream = cStringIO.StringIO()
        stereocodeDoc(tree).write(output_stream)

        cfg = configuration(
            mode=MODE_REDOCUMENT_SOURCE,
            input_from=cStringIO.StringIO(output_stream.getvalue()),
            output_to=cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = cStringIO.StringIO(),
            unique_histogram_stream = None,
            
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = True,
            extract_func_list=None
        )
        run_stereocode(cfg)
        transformed_archive_stream = cStringIO.StringIO(cfg.output_stream.getvalue())
        no_stereotype_archive = et.parse(transformed_archive_stream)
        transformed_archive_stream.close()
        located_stereotypes = no_stereotype_archive.xpath("//src:comment[contains(text(), '@stereotype')]", namespaces=xmlNamespaces)
        self.assertEqual(
            0,
            len(located_stereotypes),
            "Didn't locate correct # of namespaces within document. Located #: {0}\n\nLocated Stereotypes: \n{1}".format(
                len(located_stereotypes),
                "\n".join([et.tostring(elem) for elem in located_stereotypes])
            )
        )
        self.parse_extract_histogram(cStringIO.StringIO(cfg.histogram_stream.getvalue()), {'collaborator': 1, 'nonconstget': 1, 'get': 1})        


    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    def test_run_stereocode_remove_redocument_unique_histogram(self, tree):
        output_stream = cStringIO.StringIO()
        stereocodeDoc(tree).write(output_stream)

        cfg = configuration(
            mode=MODE_REDOCUMENT_SOURCE,
            input_from=cStringIO.StringIO(output_stream.getvalue()),
            output_to=cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = None,
            unique_histogram_stream = cStringIO.StringIO(),
            
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = True,
            extract_func_list=None
        )
        run_stereocode(cfg)
        transformed_archive_stream = cStringIO.StringIO(cfg.output_stream.getvalue())
        no_stereotype_archive = et.parse(transformed_archive_stream)
        transformed_archive_stream.close()
        located_stereotypes = no_stereotype_archive.xpath("//src:comment[contains(text(), '@stereotype')]", namespaces=xmlNamespaces)
        self.assertEqual(
            0,
            len(located_stereotypes),
            "Didn't locate correct # of namespaces within document. Located #: {0}\n\nLocated Stereotypes: \n{1}".format(
                len(located_stereotypes),
                "\n".join([et.tostring(elem) for elem in located_stereotypes])
            )
        )
        self.parse_extract_histogram(cStringIO.StringIO(cfg.unique_histogram_stream.getvalue()), {'collaborator get': 1, 'nonconstget': 1})
        
   







    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #          Testing the XmlAttr Mode of annotation
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    def test_run_stereocode_redocument_XmlAttr(self, tree):
        output_stream = cStringIO.StringIO()
        output_stream.write(et.tostring(tree))
        cfg = configuration(
            mode = MODE_ADD_XML_ATTR,
            input_from = cStringIO.StringIO(output_stream.getvalue()),
            output_to = cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = None,
            unique_histogram_stream = None,
            
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = False,
            extract_func_list = None
        )
        run_stereocode(cfg)
        transformed_doc = et.XML(cfg.output_stream.getvalue())
        # print et.tostring(transformed_doc)
        located_stereotypes = transformed_doc.xpath("//src:function[@stereotype]", namespaces=xmlNamespaces)
        self.assertEqual(
            2,
            len(located_stereotypes),
            "Didn't locate correct # of namespaces within document. Located #: {0}\n\nLocated Stereotypes: \n{1}".format(
                len(located_stereotypes),
                "\n".join([et.tostring(elem) for elem in located_stereotypes])
            )
        )


    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    def test_remove_stereotype_XmlAttr(self, tree):
        output_stream = cStringIO.StringIO()
        stereocodeDoc(tree).write(output_stream)

        cfg = configuration(
            mode=MODE_ADD_XML_ATTR,
            input_from=cStringIO.StringIO(output_stream.getvalue()),
            output_to=cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = None,
            unique_histogram_stream = None,
            
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = False,
            extract_func_list=None
        )
        remove_stereotypes(cfg)
        transformed_archive_stream = cStringIO.StringIO(cfg.output_stream.getvalue())
        no_stereotype_archive = et.parse(transformed_archive_stream)
        transformed_archive_stream.close()
        located_stereotypes = no_stereotype_archive.xpath("//src:function[@stereotype]", namespaces=xmlNamespaces)
        self.assertEqual(
            0,
            len(located_stereotypes),
            "Didn't locate correct # of namespaces within document. Located #: {0}\n\nLocated Stereotypes: \n{1}".format(
                len(located_stereotypes),
                "\n".join([et.tostring(elem) for elem in located_stereotypes])
            )
        )





    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #    Testing the reading in of additional files to
    #   use as parameters for the stereocode style sheet
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    @gen_managed_file("test_known_namespace_parsing.txt", """std
        ns1
        ns2::ns3::ns4

        """)
    def test_known_namespaces_parsing(self, filename, tree):

        output_stream = cStringIO.StringIO()
        stereocodeDoc(tree).write(output_stream)
        cfg = configuration(
            mode=MODE_ADD_XML_ATTR,
            input_from=cStringIO.StringIO(output_stream.getvalue()),
            output_to=cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = cStringIO.StringIO(),
            unique_histogram_stream = None,
            no_redocumentation = True,
            ns_prefix_stream = open(filename, "r"),
            remove_redoc = False,
            extract_func_list=None
        )
        run_stereocode(cfg)
        self.assertEqual(3, len(cfg.known_namespaces), "Incorrect # of namespaces read in.")
        self.assertEqual("std", cfg.known_namespaces[0], "Incorrect namespace.")
        self.assertEqual("ns1", cfg.known_namespaces[1], "Incorrect namespace.")
        self.assertEqual("ns2::ns3::ns4", cfg.known_namespaces[2], "Incorrect namespace.")


    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    @gen_managed_file("test_ignorable_calls.txt", """func
        less
        something

        """)
    def test_more_ignorable_calls(self, filename, tree):

        output_stream = cStringIO.StringIO()
        stereocodeDoc(tree).write(output_stream)
        cfg = configuration(
            mode=MODE_ADD_XML_ATTR,
            input_from=cStringIO.StringIO(output_stream.getvalue()),
            output_to=cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = cStringIO.StringIO(),
            unique_histogram_stream = None,
            no_redocumentation = True,
            ns_prefix_stream = None,
            more_ignorable_calls_stream=open(filename, "r"),
            remove_redoc = False,
            extract_func_list=None
        )
        run_stereocode(cfg)
        self.assertEqual(3, len(cfg.ignorable_calls), "Incorrect # of Ignorable function call names.")
        self.assertEqual("func", cfg.ignorable_calls[0], "Incorrect value.")
        self.assertEqual("less", cfg.ignorable_calls[1], "Incorrect value.")
        self.assertEqual("something", cfg.ignorable_calls[2], "Incorrect value.")


    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    @gen_managed_file("test_more_modifiers.txt", """func
        less
        something

        """)
    def test_more_modifiers(self, filename, tree):

        output_stream = cStringIO.StringIO()
        stereocodeDoc(tree).write(output_stream)
        cfg = configuration(
            mode=MODE_ADD_XML_ATTR,
            input_from=cStringIO.StringIO(output_stream.getvalue()),
            output_to=cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = cStringIO.StringIO(),
            unique_histogram_stream = None,
            no_redocumentation = True,
            ns_prefix_stream = None,
            more_modifiers_stream=open(filename, "r"),
            remove_redoc = False,
            extract_func_list=None
        )
        run_stereocode(cfg)
        self.assertEqual(3, len(cfg.modifiers), "Incorrect # modifiers.")
        self.assertEqual("func", cfg.modifiers[0], "Incorrect value.")
        self.assertEqual("less", cfg.modifiers[1], "Incorrect value.")
        self.assertEqual("something", cfg.modifiers[2], "Incorrect value.")


    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    @gen_managed_file("more_native_types.txt", """func
        less
        something

        """)
    def test_more_native_types(self, filename, tree):

        output_stream = cStringIO.StringIO()
        stereocodeDoc(tree).write(output_stream)
        cfg = configuration(
            mode=MODE_ADD_XML_ATTR,
            input_from=cStringIO.StringIO(output_stream.getvalue()),
            output_to=cStringIO.StringIO(),
            output_verbose = False,
            output_timings = False,
            histogram_stream = cStringIO.StringIO(),
            unique_histogram_stream = None,
            no_redocumentation = True,
            ns_prefix_stream = None,
            more_native_stream=open(filename, "r"),
            remove_redoc = False,
            extract_func_list=None
        )
        run_stereocode(cfg)
        self.assertEqual(3, len(cfg.native_types), "Incorrect # of native types.")
        self.assertEqual("func", cfg.native_types[0], "Incorrect value.")
        self.assertEqual("less", cfg.native_types[1], "Incorrect value.")
        self.assertEqual("something", cfg.native_types[2], "Incorrect value.")