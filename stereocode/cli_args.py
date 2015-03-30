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

def parse_cli_arguments(argumentString=None):
    """
    parse_cli_arguments - parse arguments from the command line. This returns
    a namespace object which can be validated for more complex logical interactions
    with the other program options.

    The argumentString parameter is used instead of sys.argv when it's not
    set to None.
    """

    # Loading Help documentation.
    arg_parser = argparse.ArgumentParser(
        prog="stereocode",
        description = 
"""Annotate functions/methods with special different stereotypes.
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
    arg_parser.add_argument("-i,--input", metavar='N', type=int, nargs='+', help='an integer for the accumulator')

    # parser.print_help()
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                    const=sum, default=max,
    #                    help='sum the integers (default: find the max)')

    return arg_parser.parse_args(argumentString.split() if argumentString != None else None)
