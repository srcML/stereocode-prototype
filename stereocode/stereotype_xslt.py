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

# Example code using extension functions that doesn't work due to
# a bug within lxml.
# _ns = et.FunctionNamespace(None)

# class MyExt:
#     def function1(self, ctxt, arg):
#         return '1' + arg
#     def function2(self, ctxt, arg):
#         return '2' + arg
#     def function3(self, ctxt, arg):
#         return '3' + arg

# ext_module = MyExt()
# functions = ('function1', 'function2')
# extensions = et.Extension( ext_module, functions, ns="http://www.sdml.info/srcML/src" )

# stereocodeDoc = et.XSLT(et.parse(_xsltFile), extensions=extensions)


def remove_stereotypes(config):
    # TODO: Use srcML to make this work in the future.
    # TODO: Configure stylesheet parameters.
    if config.mode == MODE_REDOCUMENT_SOURCE:
        pass
    elif config.mode ==MODE_ADD_XML_ATTR:
        raise NotImplementedError("XML node attribute not implemented as part of redocumentation yet.")
    else:
        raise Exception("Invalid Configuration Mode.")
    input_doc = et.parse(config.input_stream)
    transformed_doc = removeStereotypeDoc(input_doc)
    transformed_doc.write(config.output_stream)

def apply_stereotyping(config):
    # TODO: Use srcML to make this work in the future.
    # TODO: Configure stylesheet parameters.
    if config.mode == MODE_REDOCUMENT_SOURCE:
        pass
    elif config.mode ==MODE_ADD_XML_ATTR:
        raise NotImplementedError("XML node attribute not implemented as part of redocumentation yet.")
    else:
        raise Exception("Invalid Configuration Mode.")
    stereocodeDoc(et.parse(config.input_stream)).write(config.output_stream if config.temp_output_stream == None else config.temp_output_stream)
