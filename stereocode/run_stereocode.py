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


def run_stereocode(cli_arguments=None):
    # Loading configuration and displaying things correctly.
    try:
        config = parse_cli_arguments(cli_arguments)
    except cli_error as e:
        print >> sys.stderr, "Encountered an error from the command line", str(e)
        sys.exit(0)

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

    # Loading extractors into a list so they can be more easily accessed.
    if config.output_histogram:
        extractors.append(histogram_extractor)
    if config.output_unique_histogram:
        extractors.append(unique_histogram_extractor)
    if config.output_report:
        extractors.append(report_extractor)


    def run_extraction(filename_or_stream):
        if len(extractors) > 0:
            run_info_extractor(filename_or_stream, extractors, config.mode)
            for extractor in extractors:
                extractor.output_data(config)

    to_be_run = []
    if config.no_redoc:
        print >> sys.stderr, "Handling the situation where we process an input file."
        def extraction_no_redoc():
            run_extraction(config.input_stream)
        to_be_run.append(extraction_no_redoc)
        
    elif config.remove_redoc:
        print >> sys.stderr, "Removing redoc from source code."
        if len(extractors) > 0:
            output_file_name = "stereotype_preremoval.xml"

            def output_current_stream_into_temp():
                temp_file = open(output_file_name, "w")
                for l in config.input:
                    temp_file.write(l)
                temp_file.close()

            def extraction_remove_redoc():
                run_extraction(output_file_name)

            def delete_file():
                os.remove(output_file_name)
            to_be_run.append(output_current_stream_into_temp)
            to_be_run.append(extraction_remove_redoc)
            to_be_run.append(delete_file)
        def remove_redoc():
            raise NotImplementedError("Not implemented yet still working on it!!!")
        to_be_run.append(remove_redoc)

    else:
        print >> sys.stderr, "Performing redocumentation on input."
        if len(extractors) > 0:
            output_file_name = "stereotype_post_redoc.xml"
            def output_current_stream_into_temp():
                temp_file = open(output_file_name, "w")
                for l in config.input:
                    temp_file.write(l)
                temp_file.close()

            def extraction_remove_redoc():
                run_extraction(output_file_name)

            def delete_file():
                os.remove(output_file_name)


            to_be_run.append(output_current_stream_into_temp)
            to_be_run.append(extraction_remove_redoc)
            to_be_run.append(delete_file)
        def do_redoc():
            raise NotImplementedError("Not Implemented yet, ")
        to_be_run.append(do_redoc)


    for operation in to_be_run:
        operation()



