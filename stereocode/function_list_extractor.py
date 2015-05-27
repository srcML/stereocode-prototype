##
# @file function_list_extractor.py
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

class function_list_extractor(extractor_base):
    """
    Class that extracts a list of functions signatures by stereotype and outputs them
    into a specified file.
    """
    def __init__(self):
        super(function_list_extractor, self).__init__()
        self.histogram = dict()


    def on_function(self, stereotype_list, function_name, function_signature, document_locator, info):
        for stereotype in stereotype_list:
            if stereotype in self.histogram:
                self.histogram[stereotype] += 1
            else:
                self.histogram[stereotype] = 1

    def output_data(self, config, **kwargs):
        write_histogram("Stereotype Occurrence Histogram", self.histogram, config.histogram_stream)
