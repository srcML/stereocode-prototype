##
# @file histogram_helpers.py
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


def write_histogram(histogram_title, histogram_dict, output_stream):
    """
    Write a histogram as formatted output into the provided stream.
    """

    output_stream.write(80*"-")
    output_stream.write("\n")
    output_stream.write("{0:^80}\n".format(histogram_title))
    output_stream.write(80*"-")
    output_stream.write("\n")


    sorted_histogram = sorted(histogram_dict.items(), key=lambda x: x[1])
    for item in sorted_histogram:
        output_stream.write("  {1:>6}: {0}\n".format(*item))