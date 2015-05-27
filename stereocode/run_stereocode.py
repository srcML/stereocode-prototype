##
# @file stereocode.py
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
import os, sys
from stereotype_xslt import *
from histogram_extractor import *
from unique_histogram_extractor import *
from report_extractor import *
from function_list_extractor import *
from time import *

def run_stereocode(config):
    """
    Takes a configuration object and uses that to execute the main
    part of stereocode. There are preconditions on this function
    that are NOT enforced within this function and are instead
    enforeced within the parse_cli_arguments function.
    """

    # Using the configuration options in order to set things up for actually executing
    # stereocode.

    knownNamespaces = []

    # Reading in namespace names from file if necessary.
    if config.has_ns_pefix_file:
        knownNamespaces = config.ns_prefix_stream.read_lines()
        # TODO: Post processing on possible namespace prefixes.
        raise NotImplementedError("Namespace prefix support isn't implemented yet.")

    """
    Things that need to be figured out.
    1) What's the report going to contain?
    2) When producing the necessary output for things like
        histograms or reports can this be done all at the same time?
    3) What's the most efficient way to remove redocumentation from an archive?
    4) How much of this can be done with SAX?
    """

    extractors = []

    compute_timings = config.output_timings
    extractor_extra_data = dict()


    # Loading extractors into a list so they can be more easily accessed.
    if config.output_histogram:
        extractors.append(histogram_extractor())
    if config.output_unique_histogram:
        extractors.append(unique_histogram_extractor())
    if config.extract_function_list:
        extractors.append(function_list_extractor())
    if config.output_report:
        compute_timings = True
        extractors.append(report_extractor())



    def run_extraction(filename_or_stream):
        if len(extractors) > 0:
            if compute_timings:
                start_extraction_time = time()
            run_info_extractor(filename_or_stream, extractors, config.mode)
            if compute_timings:
                extractor_extra_data["extractor_timing"] = time() - start_extraction_time

    to_be_run = []
    if config.no_redoc:
        if config.verbose_output:
            print >> sys.stderr, "Extracting information from input archive."
        def extraction_no_redoc():
            run_extraction(config.input_stream)
        to_be_run.append(extraction_no_redoc)
        
    elif config.remove_redoc:
        if config.verbose_output:
            print >> sys.stderr, "Removing redoc from source code."
        if len(extractors) > 0:
            output_file_name = "stereotype_preremoval.xml"

            def output_current_stream_into_temp():
                temp_file = open(output_file_name, "w")
                for l in config.input_stream:
                    temp_file.write(l)
                temp_file.close()
                config.temp_input_stream = open(output_file_name, "r")

            def extraction_remove_redoc():
                run_extraction(output_file_name)

            def delete_file():
                os.remove(output_file_name)
            to_be_run.append(output_current_stream_into_temp)
            to_be_run.append(extraction_remove_redoc)
            to_be_run.append(delete_file)

        def remove_redoc():
            remove_stereotypes(config)
        to_be_run.append(remove_redoc)

    else:
        if config.verbose_output:
            print >> sys.stderr, "Performing redocumentation on input."
        if len(extractors) > 0:
            output_file_name = "stereotype_post_redoc.xml"
            def do_redoc_has_extractors():
                temp_output_stream = open(output_file_name, "w")
                # Overriding default output with my own output stream.
                config.temp_output_stream = temp_output_stream
                apply_stereotyping(config)
                temp_output_stream.close()

            def extraction_remove_redoc():
                run_extraction(output_file_name)

            def delete_temp_file():
                for l in open(output_file_name, "r"):
                    config.output_stream.write(l)
                os.remove(output_file_name)


            to_be_run.append(do_redoc_has_extractors)
            to_be_run.append(extraction_remove_redoc)
            to_be_run.append(delete_temp_file)

        else:
            def do_redoc_no_extractors():
                apply_stereotyping(config)
            to_be_run.append(do_redoc_no_extractors)

    if compute_timings:
        start_execution_time = time()

    for operation in to_be_run:
        operation()

    if compute_timings:
        extractor_extra_data["execution_time"] = time() - start_execution_time
        if config.output_timings:
            print >> sys.stderr, "Time elapsed: ", extractor_extra_data["execution_time"]

    for extractor in extractors:
        extractor.output_data(config, **extractor_extra_data)
