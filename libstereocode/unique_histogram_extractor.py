##
# @file unique_histogram_extractor.py
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

from info_extractor import *
from histogram_helpers import *

class unique_histogram_extractor(extractor_base):
    """
    Class Responsible for extracting unique stereotype groupings and constructing a histogram
    that can be output into a given stream.
    """
    def __init__(self):
        super(unique_histogram_extractor, self).__init__()
        self.histogram = dict()


    def on_function(self, stereotype_list, function_name, function_signature, document_locator, info):
        temp_unique_stereotype = " ".join(sorted(stereotype_list))
        if temp_unique_stereotype in self.histogram:
            self.histogram[temp_unique_stereotype] += 1
        else:
            self.histogram[temp_unique_stereotype] = 1

    def output_data(self, config, **kwargs):
        write_histogram("Unique Stereotype Occurrence Histogram", self.histogram, config.unique_histogram_stream)


