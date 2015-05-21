##
# @file test_decorators.py
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

import os

def gen_managed_file(filename, content):
    def run(func):
        def delete_files():
            if os.path.exists(filename):
                os.remove(filename)

        def make_call(self):
            delete_files()
            try:
                temp_strm = open(filename, "w")
                temp_strm.write(content)
                temp_strm.close()
                func(self, filename)
            except:
                delete_files()
                raise
            delete_files()
        return make_call
    return run
