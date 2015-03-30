#!/usr/bin/python
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



__doc__ = """

The main file that's used for executing stereocode from the command line.
    * This file handles the following:
    1) Command-line parameter handling
    2) I/O interfacing with an archive/file/Collection of source code files/pipes
        then handing that off to srcML to be annotated/processed.
    3) Outputting to either the command line, file or archive as desired.


"""


import srcml, sys, os, os.path, logging, argparse
from stereocode import *




if __name__ == "__main__":


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
    arg_parser.add_argument("-i,--input", metavar='N', type=int, nargs='+', help='an integer for the accumulator')

    # parser.print_help()
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                    const=sum, default=max,
    #                    help='sum the integers (default: find the max)')

    args = arg_parser.parse_args()
    # if 

    # print args.accumulate(args.integers)

    # sys.argv

    # logging.basicConfig(level=logging.INFO)
    # logger = logging.getLogger(__name__)
    # logger.debug("Starting to processing arguments")

    # Configuring argument parsing.
    # 

    # logger.debug("Completed argument processing")
    #raise NotImplementedError("Haven't started implemented this just yet.")