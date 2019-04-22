##
# @file xslt_decorators.py
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

import  lxml, lxml.etree as et, os.path, unittest
from srcml import *

def srcMLifyCode(fileToProcess, language=LANGUAGE_CXX):
    """
    Run provided source code through srcML and hand the file off
    to the decorated function so that the data can be freed after
    the call is completed.
    """
    def decorationFunc(func):
        assert os.path.exists(fileToProcess), "supplied file doesn't exist. {0}".format(fileToProcess)
        def run(self):

            try:
                with memory_buffer() as buff:
                    with writable_archive(writable_archive_settings(default_language=language), buffer=buff) as archive_writer:
                        u = archive_writer.create_unit(filename=fileToProcess)
                        u.parse(filename=fileToProcess)
                        archive_writer.write(u)
                    srcMLXmlDoc = et.XML(str(buff))
                    func(self, srcMLXmlDoc)
            except:
                print "-" * 80
                print "An error occurred within: %s"% func.__name__
                print "-" * 80
                # print "srcML:\n%s" % et.tostring(srcMLXmlDoc)
                raise
        return run
    return decorationFunc

import unittest

def expect_exception(exception_type, extra_test=None):
    """
    This is used as a decorator of a test that check if a particular type of
    exception was thrown. If no exception is throw the test is failed in by the
    decorator but if the test raises an exception of the incorrect type 
    that exception is raised again so that the error is visible.
    """
    def exception_test(func):
        def instance_extraction(self):
            try:
                func(self)
                self.assertTrue(False, "Didn't catch expected exception from function: {0}".format(func.__name__))
            except Exception as e:
                if not isinstance(e, exception_type):
                    raise
                self.assertTrue(isinstance(e, exception_type), "Incorrect exception returned. Expected type: {0}. Actual Type: {1}".format(exception_type.__name__, e.__class__.__name__))
                if extra_test is not None:
                    extra_test(self, e)
        return instance_extraction
    return exception_test


def cleanup_files(*files_to_cleanup):
    """
    Deletes a file after a test completes. Failure or no failure.
    """
    def cleanup_func(func):

        def delete_files():
            for f in files_to_cleanup:
                if os.path.exists(f):
                    os.remove(f)

        def make_call(*args):
            delete_files()
            try:
                func(*args)
            except:
                delete_files()
                raise
            delete_files()
        return make_call
    return cleanup_func