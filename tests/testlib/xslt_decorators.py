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

import  lxml, lxml.etree as et, os.path
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
                        u = archive_writer.create_unit()
                        u.parse(filename=fileToProcess)
                        archive_writer.write(u)
                    srcMLXmlDoc = et.XML(str(buff))
                    func(self, srcMLXmlDoc)
            except:
                print "-" * 80
                print "An error occurred within: %s"% func.__name__
                print "-" * 80
                print "srcML:\n%s" % et.tostring(srcMLXmlDoc)
                raise
        return run
    return decorationFunc

