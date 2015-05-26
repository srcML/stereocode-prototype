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



class TestRunStereocode(unittest.TestCase):
    
    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    def test_remove_stereotype(self, tree):
        output_stream = cStringIO.StringIO()
        stereocodeDoc(tree).write(output_stream)

        class faux_config:pass
        cfg = faux_config()
        cfg.input_stream = cStringIO.StringIO(output_stream.getvalue())
        cfg.output_stream = cStringIO.StringIO()
        cfg.mode = MODE_REDOCUMENT_SOURCE
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
            report_stream = None,
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = False
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
            report_stream = None,
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = True
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
            report_stream = None,
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = False
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
            report_stream = None,
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = False
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
    def test_run_stereocode_redocument_report(self, tree):
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
            report_stream = cStringIO.StringIO(),
            no_redocumentation = False,
            ns_prefix_stream = None,
            remove_redoc = False
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


    # @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    # def test_run_stereocode_remove_redocument_histogram(self, tree):
    #     output_stream = cStringIO.StringIO()
    #     output_stream.write(et.tostring(tree))

    #     cfg = configuration(
    #         mode=MODE_REDOCUMENT_SOURCE,
    #         input_from=cStringIO.StringIO(output_stream.getvalue()),
    #         output_to=cStringIO.StringIO(),
    #         output_verbose = False,
    #         output_timings = False,
    #         histogram_stream = None,
    #         unique_histogram_stream = None,
    #         report_stream = None,
    #         no_redocumentation = False,
    #         ns_prefix_stream = None,
    #         remove_redoc = False
    #     )

    #     run_stereocode(cfg)

    #     transformed_doc = et.XML(cfg.output_stream.getvalue())
    #     located_stereotypes = transformed_doc.xpath("//src:comment[contains(text(), '@stereotype')]", namespaces=xmlNamespaces)
    #     self.assertEqual(
    #         2,
    #         len(located_stereotypes),
    #         "Didn't locate correct # of namespaces within document. Located #: {0}\n\nLocated Stereotypes: \n{1}".format(
    #             len(located_stereotypes),
    #             "\n".join([et.tostring(elem) for elem in located_stereotypes])
    #         )
    #     )


    # @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    # def test_run_stereocode_remove_redocument_unique_histogram(self, tree):
    #     output_stream = cStringIO.StringIO()
    #     output_stream.write(et.tostring(tree))

    #     cfg = configuration(
    #         mode=MODE_REDOCUMENT_SOURCE,
    #         input_from=cStringIO.StringIO(output_stream.getvalue()),
    #         output_to=cStringIO.StringIO(),
    #         output_verbose = False,
    #         output_timings = False,
    #         histogram_stream = None,
    #         unique_histogram_stream = None,
    #         report_stream = None,
    #         no_redocumentation = False,
    #         ns_prefix_stream = None,
    #         remove_redoc = False
    #     )

    #     run_stereocode(cfg)

    #     transformed_doc = et.XML(cfg.output_stream.getvalue())
    #     located_stereotypes = transformed_doc.xpath("//src:comment[contains(text(), '@stereotype')]", namespaces=xmlNamespaces)
    #     self.assertEqual(
    #         2,
    #         len(located_stereotypes),
    #         "Didn't locate correct # of namespaces within document. Located #: {0}\n\nLocated Stereotypes: \n{1}".format(
    #             len(located_stereotypes),
    #             "\n".join([et.tostring(elem) for elem in located_stereotypes])
    #         )
    #     )
        
    # @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    # def test_run_stereocode_remove_redocument_report(self, tree):
    #     output_stream = cStringIO.StringIO()
    #     output_stream.write(et.tostring(tree))

    #     cfg = configuration(
    #         mode=MODE_REDOCUMENT_SOURCE,
    #         input_from=cStringIO.StringIO(output_stream.getvalue()),
    #         output_to=cStringIO.StringIO(),
    #         output_verbose = False,
    #         output_timings = False,
    #         histogram_stream = None,
    #         unique_histogram_stream = None,
    #         report_stream = None,
    #         no_redocumentation = False,
    #         ns_prefix_stream = None,
    #         remove_redoc = False
    #     )

    #     run_stereocode(cfg)

    #     transformed_doc = et.XML(cfg.output_stream.getvalue())
    #     located_stereotypes = transformed_doc.xpath("//src:comment[contains(text(), '@stereotype')]", namespaces=xmlNamespaces)
    #     self.assertEqual(
    #         2,
    #         len(located_stereotypes),
    #         "Didn't locate correct # of namespaces within document. Located #: {0}\n\nLocated Stereotypes: \n{1}".format(
    #             len(located_stereotypes),
    #             "\n".join([et.tostring(elem) for elem in located_stereotypes])
    #         )
    #     )