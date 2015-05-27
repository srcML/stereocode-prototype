##
# @file cli_args.py
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

import sys, os.path, logging, argparse, traceback


MODE_REDOCUMENT_SOURCE = "ReDocSrc"
MODE_ADD_XML_ATTR = "XmlAttr"
# MODE_FUNCTION_LIST = "FuncList"


processingModes = [
    MODE_REDOCUMENT_SOURCE,
    MODE_ADD_XML_ATTR
    # ,    MODE_FUNCTION_LIST
]


class configuration(object):
    """
    This is the class responsible for managing the configuration that's
    created by parse_cli_arguments. The configuration is stored within this
    class and is immutable after because it shouldn't be modified after
    the configuration is complete. 
    """
    def __init__(self, **kwargs):
        super(configuration, self).__init__()
        self._mode = kwargs["mode"]
        self._input_strm = kwargs["input_from"]
        self._output_strm = kwargs["output_to"]
        self._verbose = kwargs["output_verbose"]
        self._output_timings = kwargs["output_timings"]
        self._histogram_strm = kwargs["histogram_stream"]
        self._unique_histogram_strm = kwargs["unique_histogram_stream"]
        self._report_strm = kwargs["report_stream"]
        self._no_redoc = kwargs["no_redocumentation"]
        # self._extract_ns = kwargs["extract_ns_from_archive"]
        self._ns_pefix_file_strm = kwargs["ns_prefix_stream"]
        self._remove_redoc = kwargs["remove_redoc"]
        self._temp_output_stream = None
        self._temp_input_stream = None
        self._func_list_stream = kwargs["extract_func_list"]

    @property
    def temp_output_stream(self):
        return self._temp_output_stream
    @temp_output_stream.setter
    def temp_output_stream(self, value):
        self._temp_output_stream = value
    

    @property
    def temp_input_stream(self):
        return self._temp_input_stream
    @temp_input_stream.setter
    def temp_input_stream(self, value):
        self._temp_input_stream = value
    
    @property
    def mode(self):
        return self._mode

    @property
    def input_stream(self):
        return self._input_strm

    @property
    def output_stream(self):
        return self._output_strm

    @property
    def verbose_output(self):
        return self._verbose

    @property
    def output_timings(self):
        return self._output_timings

    @property
    def output_histogram(self):
        return self._histogram_strm != None

    @property
    def histogram_stream(self):
        return self._histogram_strm

    @property
    def output_unique_histogram(self):
        return self._unique_histogram_strm != None

    @property
    def unique_histogram_stream(self):
        return self._unique_histogram_strm

    @property
    def output_report(self):
        return self._report_strm != None

    @property
    def report_stream(self):
        return self._report_strm

    @property
    def extract_function_list(self):
        return self._func_list_stream != None

    @property
    def function_list_stream(self):
        return self._func_list_stream
    
    # @property
    # def extract_ns_from_archive(self):
    #     return self._extract_ns
    
    @property
    def has_ns_pefix_file(self):
        return self._ns_pefix_file_strm != None

    @property
    def ns_pefix_file_stream(self):
        return self._ns_pefix_file_strm

    @property
    def no_redoc(self):
        return self._no_redoc

    @property
    def remove_redoc(self):
        return self._remove_redoc



class cli_error(Exception):
    """
    Command line interface error. This is throw by parse_cli_arguments when
    there is a violation of a precondition of one of the arguments so that
    the help message can be displayed and output.
    """
    def __init__(self, cli_argument_name, message, value=None, *nargs):
        super(cli_error, self).__init__(cli_argument_name, message, value, *nargs)
        self.cli_name = cli_argument_name
        self.error_message = message

def parse_cli_arguments(argument_string=None, output_help_on_failure=True):
    """
    parse_cli_arguments - parse arguments from the command line. This returns
    a namespace object which can be validated for more complex logical interactions
    with the other program options.

    The argument_string parameter is used instead of sys.argv when it's not
    set to None.

    output_help_on_failure - Is used to prevent the output of a help message
    in the event that there is a failure with a precondition from the
    provided arguments. The default is to always output the help message before throwing
    an exception.
    """

    """
    -------------------------------------------------------
                            NOTES
    -------------------------------------------------------
    Needed CLI Arguments:
        * input type - Default stdin. Possibly inferred via input type.
        * output type - Defaults to stdout. Outputs to that or a file.
        * Processing Mode - Defaults to source code annotating.
            1) Source Code Re-documentation. Annotate the current source code itself with a
                comment containing @stereotype followed by the stereotypes of that function.
            2) XML Attribute Annotation. Each <function> is annotated with stereotype XML 
                attribute that contains a comma separated list of stereotypes associated
                with that method.
            3) Function List. Creates a new archive containing an XML archive containing
                a list of all function signatures by file paired with stereotype
                information.
        * Maybe formatting for comment/attribute given in the form of python
            string formatting.

        * Should this work with a URI?!?!?

    Optional CLI arguments:
        * Namespace file - For giving a list of known namespaces.
        * Basic types file - a file for listing the names of basic types which are to be used while processing
            stereotyes.
        * 
    """

    # Loading Help documentation.
    arg_parser = argparse.ArgumentParser(
        prog="stereocode",
        description = 
"""
Annotate functions/methods with special different stereotypes.
The expected input to is a srcML archive.


This program has several methods of operation:
    1) Source Code Re-documentation. Annotate the current source code itself with a
        comment containing @stereotype followed by the stereotypes of that function.
    2) XML Attribute Annotation. Each <function> is annotated with stereotype XML 
        attribute that contains a comma separated list of stereotypes associated
        with that method.
    3) Function List. Creates a new archive containing an XML archive containing
        a list of all function signatures by file paired with stereotype
        information.
"""
    )


    # Loading arguments.
    arg_parser.add_argument(
        "-i",
        "--input",
        metavar='INPUT',
        type=str,
        default=None,
        help='Specify the input type. The default is to use stdin as the input. The input should be specified as a file path.'
    )
    
    arg_parser.add_argument(
        "-o",
        "--output",
        metavar='OUTPUT',
        type=str,
        nargs='?',
        default=None,
        dest="output",
        help="Specify the output type. The default is to use stdout as the output. The output should be specified as a path to a file."
    )

    arg_parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default=processingModes[0],
        choices=processingModes,
        dest="mode",
        help='Specifies how the output should be formatted. possible modes: ReDocSrc, XmlAttr, and FuncList.'
    )

    arg_parser.add_argument(
        "-v",
        "--verbose",
        action='store_true',
        default=False,
        dest="debug",
        help='Enables logging of debug information.'
    )

    arg_parser.add_argument(
        "-t",
        "--enable-timing",
        action='store_true',
        default=False,
        dest="enableTiming",
        help='Outputs execution timing information to the console. This information is included as part of the report if generated.'
    )

    arg_parser.add_argument(
        "--histogram",
        metavar='HISTOGRAM_PATH',
        type=str,
        default=None,
        dest="computeHistogram",
        help="Output counts of all occurrences of each type stereotype. Setting this outputs a count for each time a "
            +"stereotype occurs, and not for each combination of stereotypes. The output is written into a file."
            + " The input be redocumented with stereotypes unless --no-redoc is specified."
    )

    arg_parser.add_argument(
        "--unique-histogram",
        metavar='UNIQUE_HISTOGRAM_PATH',
        type=str,
        default=None,
        dest="computeUniqueHistogram",
        help="Output counts of all occurrences of each combination of stereotypes applied to a function. The input be redocumented with stereotypes unless --no-redoc is specified."
    )

    arg_parser.add_argument(
        "-n",
        "--no-redoc",
        action='store_true',
        default=False,
        dest="noRedoc",
        help="Doesn't recompute stereotypes for an input archive, but instead simply loads the input file and assumes that the archive was redocumented in the specified mode."
    )

    arg_parser.add_argument(
        "--report",
        metavar='REPORT_PATH',
        type=str,
        default=None,
        dest="generateReport",
        help="Generate a report from after an archive was transformed or from an existing archive if --no-redoc is specified."
    )

    arg_parser.add_argument(
        "--ns-file",
        metavar='NAMESPACE_PATH',
        type=str,
        default=None,
        dest="namespaceFileName",
        help="Specify possible namespace prefixes for functions. This allows for namespace that are defined within macros to be specified and prevents free functions from being mistaken as member functions. The namespaces are specified using their prefix for a function, one per line. For example std:: would be a the standard namespace prefix."
    )

    # arg_parser.add_argument(
    #     "--no-ns-pre-extract",
    #     action='store_true',
    #     default=False,
    #     dest="noExtractNs",
    #     help="Prevents the pre-extraction of namespaces from the input archive. This is used to identify member functions."
    # )

    arg_parser.add_argument(
        "--remove-redoc",
        action='store_true',
        default=False,
        dest="removeRedocumentation",
        help="This processing mode removes existing sterotypes from the provided archive. Only removes stereotypes that are part of the specified mode."
    )

    arg_parser.add_argument(
        "-f",
        "--extract-func-list",
        metavar='FUNC_LIST_PATH',
        type=str,
        default=None,
        dest="extractFunctionList",
        help="This is option allows for the stereotypes and functions from an existing archive to be extracted and output into a given file."
    )

    # Error assistance function.
    def precondition_test(cond, variable_name, failure_message, value):
        if not cond:
            if output_help_on_failure:
                arg_parser.print_help()
            raise cli_error(variable_name, failure_message, value)

    input_from = None
    output_to = None
    mode = None
    output_verbose = False
    output_timings = False
    histogram_stream = None
    unique_histogram_stream = None
    report_stream = None
    no_redocumentation = False
    ns_prefix_stream = None
    remove_redoc = False
    extract_func_list_strm = None

    args = arg_parser.parse_args(argument_string.split() if argument_string != None else None)
    no_redocumentation = args.noRedoc
    remove_redoc = args.removeRedocumentation
    mode = args.mode

    # setting trivial configuration options.
    output_verbose = args.debug
    output_timings = args.enableTiming


    # Computing constraints between multiple possible parameters
    # ----------------------------------------------------------------------------
    #       Constraints that involve more than one CLI argument
    # ----------------------------------------------------------------------------
    if remove_redoc:
        # precondition_test(mode != MODE_FUNCTION_LIST, "--mode,--remove-redoc", "Can't remove redocumentation from a function list.", args.mode)
        precondition_test(not no_redocumentation, "--no-redoc,--remove-redoc", "Invalid option combination.", None)
        precondition_test(args.namespaceFileName is None, "--ns-file,--remove-redoc", "can't use namespaces file when removing documentation", None)

    if no_redocumentation:
        # precondition_test(mode != MODE_FUNCTION_LIST, "--no-redoc,--mode", "Information can't be extracted from a function list", None)
        precondition_test(
            args.generateReport is not None or
            args.computeUniqueHistogram is not None or
            args.computeHistogram is not None or
            args.extractFunctionList is not None,
            "--no-redoc,--report,--histogram,--unique-histogram, --extract-func-list",
            "When processing a file with no redocumentation option set you must set at least one of the following options: --report, --hisogram, --unique-histogram, --extract-func-list",
            None
        )

    # ----------------------------------------------------------------------------    
    # Do this last so that I know that everything else is configured already before
    # messing with streams, what I'm trying to avoid is not closing the
    # streams in the event of an error.


    # Configuring input and output streams.
    try:
        if args.extractFunctionList is not None:
            try:
                extract_func_list_strm = open(args.extractFunctionList, "w")
            except Exception as e:
                raise cli_error("--extract-func-list", "Failed to open function list file writing", args.extractFunctionList, e)                
        if args.computeHistogram is not None:
            try:
                histogram_stream = open(args.computeHistogram, "w")
            except Exception as e:
                raise cli_error("--histogram", "Failed to open histogram file writing", args.computeHistogram, e)

        if args.computeUniqueHistogram is not None:
            try:
                unique_histogram_stream = open(args.computeUniqueHistogram, "w")
            except Exception as e:
                raise cli_error("--unique-histogram", "Failed to open unique histogram file writing", args.computeUniqueHistogram, e)

        if args.namespaceFileName is not None:
            try:
                precondition_test(os.path.exists(args.namespaceFileName), "--ns-file", "Provided input doesn't exist.", args.namespaceFileName)
                precondition_test(os.path.isfile(args.namespaceFileName), "--ns-file", "Provided input isn't a file.", args.namespaceFileName)
                ns_prefix_stream = open(args.namespaceFileName, "r")
            except Exception as e:
                raise cli_error("--ns-file", "Failed to open namespace file for reading", args.namespaceFileName, e)

        if args.generateReport is not None:
            try:
                report_stream = open(args.generateReport, "w")
            except Exception as e:
                raise cli_error("--report", "Failed to open report file writing", args.generateReport, e)


        if args.output is None:
            output_to = sys.stdout
        else:
            try:
                output_to = open(args.output, "w")
            except Exception as e:
                raise cli_error("--output", "Failed to open output file writing", args.output, e)

        if args.input is None:
            input_from = sys.stdin
        else:
            precondition_test(os.path.exists(args.input), "--input", "Provided input doesn't exist.", args.input)
            precondition_test(os.path.isfile(args.input), "--input", "Provided input isn't a file.", args.input)
            input_from = open(args.input, "r")

    except Exception as e:

        if extract_func_list_strm is not None:
            extract_func_list_strm.close()

        if histogram_stream is not None:
            histogram_stream.close()

        if unique_histogram_stream is not None:
            unique_histogram_stream.close()

        if report_stream is not None:
            report_stream.close()

        if ns_prefix_stream is not None:
            ns_prefix_stream.close()

        if args.output is not None:
            if output_to is not None:
                output_to.close()
        raise

    



    # Enforcing constraints and configuration.
    return configuration(
        mode=mode,
        input_from=input_from,
        output_to=output_to,
        output_verbose = output_verbose,
        output_timings =output_timings,
        histogram_stream = histogram_stream,
        unique_histogram_stream = unique_histogram_stream,
        report_stream = report_stream,
        no_redocumentation = no_redocumentation,
        # extract_ns_from_archive = extract_ns_from_archive,
        ns_prefix_stream = ns_prefix_stream,
        remove_redoc = remove_redoc,
        extract_func_list = extract_func_list_strm
    )
