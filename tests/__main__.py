##
# @file __main__.py
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

import unittest, sys, lxml.etree as et, lxml, os, os.path
from test_cli_args import *
from test_stereotype_xslt import *
from stereocode import *
from testlib import *

if __name__ == '__main__':

    # Handling special test cases that are run after the initial test suite so that they can
    # test a larger mount of projects.

    # Walking all of the directories and re-srcml-ing
    # each of the files from within an all archive, then
    # re-running stereocode on it and testing the result
    # to see if the stereotypes are the same or different.
    for root, dirs, files in os.walk("/home/brian/Projects/stereotypes/AllArchives"):
        dirs = [d for d in dirs if d != DataFolderName]

        for name in files:
            currentName = os.path.join(root, name)
            print currentName
    unittest.main()
