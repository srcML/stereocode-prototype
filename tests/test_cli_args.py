##
# @file test_cli_args.py
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

import unittest, sys
from stereocode import *

class TestCLIArgs(unittest.TestCase):    
    def test_default_parsed_arguments(self):
        result = parse_cli_arguments("")

        self.assertTrue(isinstance(result.input, list), "Didn't get expected type.")
        self.assertEqual(result.output, None, "Didn't get expected type.")
        self.assertEqual(result.mode,processingModes[0], "Didn't get expected type.")
        self.assertFalse(result.debug, "Didn't get expected type.")
        self.assertFalse(result.enableTiming, "Didn't get expected type.")
        
