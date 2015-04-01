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

import os.path, logging, argparse


processingModes = [
    "ReDocSrc",
    "XmlAttr",
    "FuncList"
]

# class Configuration

def parse_cli_arguments(argumentString=None):
    """
    parse_cli_arguments - parse arguments from the command line. This returns
    a namespace object which can be validated for more complex logical interactions
    with the other program options.

    The argumentString parameter is used instead of sys.argv when it's not
    set to None.
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
        "input",
        metavar='INPUT',
        type=str,
        nargs='*',
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
        help='Specifies how the output should be annotated.'
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
        action='store_true',
        default=False,
        dest="enableTiming",
        help='Outputs execution timing information.'
    )

    arg_parser.add_argument(
        "--histogram",
        action='store_true',
        default=False,
        dest="computeHistogram",
        help="Output counts of all occurrences of each type stereotype. Setting this outputs a count for each time a "
            +"stereotype occurs, and not for each combination of stereotypes."
    )

    arg_parser.add_argument(
        "--unique-histogram",
        action='store_true',
        default=False,
        dest="computeUniqueHistogram",
        help="Output counts of all occurrences of each combination of stereotypes applied to a function."
    )

    return arg_parser.parse_args(argumentString.split() if argumentString != None else None)
