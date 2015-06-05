##
# @file stereotype_xslt.py
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


import lxml.etree as et, lxml, os, os.path, sys
from cli_args import *

_currentDirectory = os.path.dirname(os.path.abspath(__file__))

stereocodeXsltFilePath = os.path.join(_currentDirectory, "xslt", "stereotype.xsl")
stereocodeDoc = et.XSLT(et.parse(stereocodeXsltFilePath))

_remove_stereotype_doc_path = os.path.join(_currentDirectory, "xslt", "remove_stereotypes.xsl")
removeStereotypeDoc = et.XSLT(et.parse(_remove_stereotype_doc_path))

def remove_stereotypes(config):
    input_doc = et.parse(config.input_stream if config.temp_input_stream == None else config.temp_input_stream)
    parameters = dict(processing_mode=et.XSLT.strparam(config.mode))
    transformed_doc = removeStereotypeDoc(input_doc, **parameters)
    if len(removeStereotypeDoc.error_log) > 0:
        print >> sys.stderr, removeStereotypeDoc
    transformed_doc.write(config.output_stream)

def apply_stereotyping(config):
    parameters = dict(processing_mode=et.XSLT.strparam(config.mode))
    if config.known_namespaces != None:
        temp = " ".join([x for x in config.known_namespaces])
        parameters["more_namespaces"] = et.XSLT.strparam(temp)

    if config.native_types != None:
        parameters["more_native"] = et.XSLT.strparam(" ".join([x for x in config.native_types]))

    if config.modifiers != None:
        parameters["more_modifiers"] = et.XSLT.strparam(" ".join([x for x in config.modifiers]))

    if config.ignorable_calls != None:
        parameters["more_ignorable_calls"] = et.XSLT.strparam(" ".join([x for x in config.ignorable_calls]))

    redocumented_doc = stereocodeDoc(et.parse(config.input_stream), **parameters)
    # if len(stereocodeDoc.error_log) > 0:
    #     print >> sys.stderr, stereocodeDoc
    redocumented_doc.write(config.output_stream if config.temp_output_stream == None else config.temp_output_stream)
