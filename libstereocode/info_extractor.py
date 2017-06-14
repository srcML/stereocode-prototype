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
import cStringIO, sys, re
from kitchen.text.converters import to_bytes



class extractor_base(object):
    """
    The base class for all classes used by
    info_extractor when traversing an archive.
    """
    def __init__(self):
        super(extractor_base, self).__init__()


    def start_document(self):
        pass

    def end_document(self):
        pass

    def on_function(self, stereotype_list, function_name, function_signature, document_locator, info):
        pass

    def on_unit(self, filename, document_locator, info):
        pass

    def end_unit(self):
        pass

    def output_data(self, config, **kwargs):
        raise NotImplementedError("This must be implemented by a base class.")




STATE_START = "STATE_START"
STATE_UNIT_SEARCH = "STATE_UNIT_SEARCH"

STATE_PROCESSING_LOOP = "STATE_PROCESSING_LOOP"

STATE_READING_COMMENT = "STATE_READING_COMMENT"

STATE_EXPECTING_FUNCTION = "STATE_EXPECTING_FUNCTION "
STATE_READING_FUNCTION_SIGNATURE = "STATE_READING_FUNCTION_SIGNATURE"

STATE_READING_TYPE_NAME = "STATE_READING_TYPE_NAME" # for when reading class, struct, union, attribute_defn or interfaces depending on the language.

# Function Reading SubState
FUNCSIG_STATE_READING_UPTHROUGH_TYPE = "FUNCSIG_STATE_READING_UPTHROUGH_TYPE"
FUNCSIG_STATE_READING_FUNCTION_NAME = "FUNCSIG_STATE_READING_FUNCTION_NAME"
FUNCSIG_STATE_READING_TILL_BLOCK = "FUNCSIG_STATE_READING_TILL_BLOCK"

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
_TAG_block = "block"
_TAG_try = 'try'
_TAG_type = "type"

# attributes
_ATTR_stereotype = "stereotype"
_ATTR_filename = "filename"
_ATTR_type = "type"

# Regular expression
stereotypeExtractingRe = re.compile(r"@stereotype (?P<stereotypes>[^\*]*)")

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


class info_extractor(object, handler.ContentHandler):
    """
    A SAX parser for coordinating multiple SAX-like interfaces
    That would each require their own individual pass but are called from
    inside the info extractor instead during a single pass.

    This is a SAX-parser that calls special SAX-like on the set of 
    extractors in a uniform manner, there by hiding the way that
    annotations were added to an archive.
    """
    def __init__(self, extractor_set, mode=MODE_REDOCUMENT_SOURCE):
        super(info_extractor, self).__init__()
        self.extractors = extractor_set
        self.document_locator = None
        self.current_unit_name = None
        self.is_archive = False
        self.cls_ns_stack = []
        self._state = STATE_START
        self.configuration_mode = mode
        self.current_stereotype = None
        self.current_function_name = None
        self.current_function_signature = None
        self.buffer = cStringIO.StringIO()
        self.function_sig_buffer = None
        self.read_content = False
        self.type_name_depth = 0
        self.function_sig_depth = 0
        self.function_name_buffer = None
        self._function_sig_state = FUNCSIG_STATE_READING_UPTHROUGH_TYPE


    @property
    def function_sig_state(self):
        return self._function_sig_state
    @function_sig_state.setter
    def function_sig_state(self, value):
        self._function_sig_state = value
    
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
    

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
        for extractor in self.extractors:
            extractor.start_document()

    def endDocument(self):
        assert self.state == STATE_UNIT_SEARCH, "Didn't exit in correct state after parsing was complete. Current State: {0}".format(self.state)
        for extractor in self.extractors:
            extractor.end_document()
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
            if (name == _TAG_class or
                name == _TAG_struct or
                name == _TAG_interface or
                name == _TAG_annotation_defn or
                name == _TAG_union):
                self.state = STATE_READING_TYPE_NAME
                self.type_name_depth = 0

            elif name == _TAG_function:
                if _ATTR_stereotype in attrs:
                    self.current_stereotype = attrs[_ATTR_stereotype].split()
                    self.state = STATE_READING_FUNCTION_SIGNATURE
                    self.function_name_buffer = cStringIO.StringIO()
                    self.function_sig_depth = 0
                    self.function_sig_state = FUNCSIG_STATE_READING_UPTHROUGH_TYPE


            elif name == _TAG_comment:
                if _ATTR_type in attrs:
                    if attrs[_ATTR_type] == "block":
                        self.state = STATE_READING_COMMENT
            pass

        elif self.state == STATE_READING_COMMENT:
            pass


        elif self.state == STATE_EXPECTING_FUNCTION:
            if name != _TAG_function:
                self.raise_error_message("Stereotype isn't next to a function. Tag encountered: {0}".format(name))
            self.state = STATE_READING_FUNCTION_SIGNATURE
            self.function_name_buffer = cStringIO.StringIO()
            self.function_sig_depth = 0
            self.function_sig_state = FUNCSIG_STATE_READING_UPTHROUGH_TYPE

        elif self.state == STATE_READING_FUNCTION_SIGNATURE:
            self.function_sig_depth += 1
            if self.function_sig_state == FUNCSIG_STATE_READING_UPTHROUGH_TYPE:
                # if function has no type such as in some operator methods
                if self.function_sig_depth == 1 and name == _TAG_name:
                    self.function_sig_state = FUNCSIG_STATE_READING_FUNCTION_NAME 
            elif self.function_sig_state == FUNCSIG_STATE_READING_FUNCTION_NAME:
                pass
            elif self.function_sig_state == FUNCSIG_STATE_READING_TILL_BLOCK:
                if name == _TAG_block or name == _TAG_try:
                    if  self.function_sig_depth == 1:
                        self.current_function_signature = self.buffer.getvalue()
                        self.buffer.close()
                        self.buffer = cStringIO.StringIO()
                        self._call_on_function(self.current_stereotype, self.current_function_name.strip(), self.current_function_signature.strip())
                        self.state = STATE_PROCESSING_LOOP

        elif self.state == STATE_READING_TYPE_NAME:

            self.type_name_depth += 1

            if name == _TAG_name:
                if self.type_name_depth == 1:
                    self.read_content = True

            # anonymous type name
            elif name == _TAG_block:
                self.read_content = False
                self.cls_ns_stack.append(self.buffer.getvalue())
                self.buffer.close()
                self.buffer = cStringIO.StringIO()
                self.state = STATE_PROCESSING_LOOP

        else:
            raise Exception ("Invalid state encountered: {0}".format(self.state))

    def endElement(self, name):
        if self.state == STATE_START:
            self.raise_error_message("Invalid end of tag. This logically should never be called. Ending Tag: {0}".format(self.name))

        elif self.state == STATE_UNIT_SEARCH:
            assert name == _TAG_unit, "Expecting to encounter an end of unit tag: Encountered: {0}".format(name)

        elif self.state == STATE_PROCESSING_LOOP:

            if (name == _TAG_class or
                name == _TAG_struct or
                name == _TAG_interface or
                name == _TAG_annotation_defn or
                name == _TAG_union):
                self.cls_ns_stack.pop()

            elif name == _TAG_unit:
                for extractor in self.extractors:
                    extractor.end_unit()
                self.cls_ns_stack = []
                self.state = STATE_UNIT_SEARCH

        elif self.state == STATE_READING_COMMENT:
            if name == _TAG_comment:

                comment_text = self.buffer.getvalue()
                # print >> sys.stderr, comment_text
                self.buffer.close()
                self.buffer = cStringIO.StringIO()
                if comment_text.find("@stereotype") != -1:
                    self.state = STATE_EXPECTING_FUNCTION

                    stereotypeMatch = stereotypeExtractingRe.search(comment_text)
                    if stereotypeMatch == None:
                        self.raise_error_message("Invalid stereotype comment, located @stereotype within an existing comment but didn't locate stereotype information.")
                    else:
                        self.current_stereotype = [x.lower() for x in stereotypeMatch.group("stereotypes").strip().split(" ")]
                else:
                    self.state = STATE_PROCESSING_LOOP

        elif self.state == STATE_EXPECTING_FUNCTION:
            pass

        elif self.state == STATE_READING_FUNCTION_SIGNATURE:
            self.function_sig_depth -= 1
            if self.function_sig_state == FUNCSIG_STATE_READING_UPTHROUGH_TYPE:
                if self.function_sig_depth == 0 and name == _TAG_type:
                    self.function_sig_state = FUNCSIG_STATE_READING_FUNCTION_NAME   
            elif self.function_sig_state == FUNCSIG_STATE_READING_FUNCTION_NAME:
                if self.function_sig_depth == 0:
                    if name == _TAG_name:
                        self.current_function_name = self.function_name_buffer.getvalue() 
                        self.function_name_buffer.close()
                        self.function_name_buffer = None
                        self.function_sig_state = FUNCSIG_STATE_READING_TILL_BLOCK
                    else:
                        pass
                        #self.raise_error_message("Encountered unexpected element while transitioning from reading function name to reading the rest of the function signature.")
                    # self.current_function_signature = 
            elif self.function_sig_state == FUNCSIG_STATE_READING_TILL_BLOCK:
                pass

        elif self.state == STATE_READING_TYPE_NAME:

            self.type_name_depth -= 1

            if name == _TAG_name and self.read_content:

                if self.type_name_depth == 0:
                    self.read_content = False
                    self.cls_ns_stack.append(self.buffer.getvalue())
                    self.buffer.close()
                    self.buffer = cStringIO.StringIO()
                    self.state = STATE_PROCESSING_LOOP

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
            self.buffer.write(to_bytes(content))

        elif self.state == STATE_EXPECTING_FUNCTION:
            pass

        elif self.state == STATE_READING_FUNCTION_SIGNATURE:
            if self.function_sig_state == FUNCSIG_STATE_READING_FUNCTION_NAME:
                self.function_name_buffer.write(to_bytes(content))
            self.buffer.write(to_bytes(content))

        elif self.state == STATE_READING_TYPE_NAME:
            if self.read_content:
                self.buffer.write(to_bytes(content))

        else:
            raise Exception ("Invalid state encountered: {0}".format(self.state))


    # Helper Functions associated with the information being extracted.
    def getCurrentUnitName(self):
        return self.current_unit_name

def run_info_extractor(filename_or_stream, extractor_set, mode=MODE_REDOCUMENT_SOURCE):
    handler = info_extractor(extractor_set, mode)
    parse(filename_or_stream, handler)