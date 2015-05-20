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
    # Loading configuration and displaying things correctly.
    try:
        config = parse_cli_arguments()
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
    # if config.has_ns_file
    if config.no_redoc:
        print "Handling the situation where we process an input file."
    elif config.remove_redoc:
        print "Removing redoc from source code."
    else:
        print "Performing redocumentation on input. This is the easiest case."


