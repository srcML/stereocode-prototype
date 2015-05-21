##
# @file info_extractor.py
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


from xml.sax.handler import *
from xml.sax import *
from cli_args import MODE_REDOCUMENT_SOURCE, MODE_ADD_XML_ATTR

class extractor_base(object):
    """
    The base class for all classes used by
    info_extractor when traversing an archive.
    """
    def __init__(self):
        super(extractor_base, self).__init__()


    def on_function(self, stereotype_list, function_name, function_signature, document_locator, info):
        pass

    def on_unit(self, filename, document_locator, info):
        pass

STATE_START = "Starting State"
STATE_UNIT_SEARCH = "Looking For Unit"

STATE_PROCESSING_LOOP = "Scanning loop and gathering info"

STATE_READING_COMMENT = "Reading comment"

STATE_EXPECTING_FUNCTION = "Expecting to encounter function or related tag."
STATE_READING_FUNCTION_SIGNATURE = "Reading Function Signature"

STATE_READING_TYPE_NAME = "Reading class name" # for when reading class, struct, union, attribute_defn or interfaces depending on the language.


# Tag and attribute constants
_TAG_unit = "unit"
_TAG_comment = "comment"
_TAG_class = "class"
_TAG_struct = "struct"
_TAG_union = "union"
_TAG_interface = "interface"
_TAG_annotation_defn = "annotation_defn"
_TAG_name = "name"
_TAG_function = "function"

# attributes
_ATTR_stereotype = "stereotype"
_ATTR_filename = "filename"

# Exceptions
class extractor_error(Exception):
    """
    Raised in the even that an error occurs during the parsing of an
    archive. Not to be used by classes other than info_extractor.
    """
    def __init__(self, state, message, *nargs):
        super(Exception, self).__init__(state, message, *nargs)
        self.state = state
        self.message = message


class info_extractor(handler.ContentHandler):
    """
    A SAX parser for coordinating multiple SAX-like interfaces
    That would each require their own individual pass but are called from
    inside the info extractor instead during a single pass.

    This is a SAX-parser that calls special SAX-like on the set of 
    extractors in a uniform manner, there by hiding the way that
    annotations were added to an archive.
    """
    def __init__(self, extractor_set, mode=MODE_REDOCUMENT_SOURCE):
        # super(handler.ContentHandler, self).__init__()
        self.extractors = extractor_set
        self.document_locator = None
        self.current_unit_name = None
        self.is_archive = False
        self.cls_ns_stack = []
        self.state = STATE_START
        self.configuration_mode = mode

    def _call_on_unit(self, unit_filename):
        self.current_unit_name = unit_filename
        for extractor in self.extractors:
            extractor.on_unit(unit_filename, self.document_locator, self)

    def _call_on_function(self, stereotype_list, function_name, function_signature):
        for extractor in self.extractors:
            extractor.on_function(stereotype_list, function_name, function_signature, self.document_locator, self)

    def raise_error_message(self, message):
        raise extractor_error(self.state, message, self.document_locator.getLineNumber())

    def startDocument(self):
        self.state = STATE_START

    def endDocument(self):
        self.state = STATE_START

    def setDocumentLocator(self, locator):
        """Save the locator so that it can be passed to the extractors."""
        self.document_locator = locator


    def startElement(self, name, attrs):
        if self.state == STATE_START:
            if name != _TAG_unit:
                self.raise_error_message("Unexpected or invalid tag. Tag name: {0}".format(name))

            if _ATTR_filename in attrs:
                self.is_archive = False
                self._call_on_unit(attrs[_ATTR_filename])
                self.state = STATE_PROCESSING_LOOP

            else:
                self.is_archive = True
                self.state = STATE_UNIT_SEARCH

        elif self.state == STATE_UNIT_SEARCH:
            if name != _TAG_unit:
                self.raise_error_message("Unexpected or invalid tag. Tag name: {0}".format(name))

            if _ATTR_filename in attrs:
                self._call_on_unit(attrs[_ATTR_filename])
            else:
                self._call_on_unit(None)
            self.state = STATE_PROCESSING_LOOP

        elif self.state == STATE_PROCESSING_LOOP:
            pass

        elif self.state == STATE_READING_COMMENT:
            pass

        elif self.state == STATE_EXPECTING_FUNCTION:
            pass

        elif self.state == STATE_READING_FUNCTION_SIGNATURE:
            pass

        elif self.state == STATE_READING_TYPE_NAME:
            pass

        else:
            raise Exception ("Invalid state encountered: {0}".format(self.state))

    def endElement(self, name):
        if self.state == STATE_START:
            self.raise_error_message("Invalid end of tag. This logically should never be called. Ending Tag: {0}".format(self.name))

        elif self.state == STATE_UNIT_SEARCH:
            assert name == _TAG_unit, "Expecting to encounter an end of unit tag: Encountered: {0}".format(name)

        elif self.state == STATE_PROCESSING_LOOP:
            pass

        elif self.state == STATE_READING_COMMENT:
            pass

        elif self.state == STATE_EXPECTING_FUNCTION:
            pass

        elif self.state == STATE_READING_FUNCTION_SIGNATURE:
            pass

        elif self.state == STATE_READING_TYPE_NAME:
            pass

        else:
            raise Exception ("Invalid state encountered: {0}".format(self.state))

    def characters(self, content):
        if self.state == STATE_START:
            pass

        elif self.state == STATE_UNIT_SEARCH:
            pass

        elif self.state == STATE_PROCESSING_LOOP:
            pass

        elif self.state == STATE_READING_COMMENT:
            pass

        elif self.state == STATE_EXPECTING_FUNCTION:
            pass

        elif self.state == STATE_READING_FUNCTION_SIGNATURE:
            pass

        elif self.state == STATE_READING_TYPE_NAME:
            pass

        else:
            raise Exception ("Invalid state encountered: {0}".format(self.state))


    # Helper Functions associated with the information being extracted.
    def getCurrentUnitName(self):
        return self.current_unit_name

def run_info_extractor(filename, extractor_set, mode=MODE_REDOCUMENT_SOURCE):
    handler = info_extractor(extractor_set, mode)
    parse(filename, handler)