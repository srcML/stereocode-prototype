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

class unit_info:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    # def __repr__(self):
    #     return str(self.__dict__) 
    def __str__(self):
        return str(self.__dict__) 

class func_info:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def __repr__(self):
        return "\n" + str(self.__dict__) 

    def __str__(self):
        return "\n" + str(self.__dict__) 

class function_list_extractor(extractor_base):
    """
    Class that extracts a list of functions signatures by stereotype and outputs them
    into a specified file.
    """
    def __init__(self):
        super(function_list_extractor, self).__init__()
        self.functions_by_unit = []
        self.current_unit = None

    
    def start_document(self):
        self.functions_by_unit = []

    def end_document(self):
        self.functions_by_unit.append(self.current_unit)
        self.current_unit = None
    
    def on_unit(self, filename, document_locator, info):
        self.current_unit = unit_info(filename=filename, archive_line_number=document_locator.getLineNumber(), functions=[])
    
    
    def on_function(self, stereotype_list, function_name, function_signature, document_locator, info):
        self.current_unit.functions.append(
            func_info(
                name=function_name,
                signature=function_signature,
                file_line_number=document_locator.getLineNumber() - self.current_unit.archive_line_number,
                archive_line_number=document_locator.getLineNumber(),
                stereotypes=stereotype_list,
                is_within_class=len(info.cls_ns_stack) !=0,
                class_name="::".join(info.cls_ns_stack)
            )
        )

    
    def output_data(self, config, **kwargs):
        # write_histogram("Stereotype Occurrence Histogram", self.histogram, config.histogram_stream)
        pass
