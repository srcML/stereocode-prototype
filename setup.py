#!/usr/bin/python
##
# @file setup.py
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

from setuptools import setup
import sys

extra = { }

if sys.version_info >= (3,):
    extra['use_2to3'] = True
    raise NotImplementedError("2to3 conversion has not been tested!")

def read_docuemntation():
    return "\n".join(open("README.md").readlines())
setup(
    name='stereocode',
    version = '1.0',
    description='Source code stereotypeing tool that annotates srcML-i-fied with method stereotypes.',
    author='SDML',
    author_email='',
    package_dir = {'stereocode': 'stereocode', 'stereocode/xslt': 'stereocode.xslt'},
    packages = ['stereocode'],
    data_files=[
        ('stereocode/xslt',
            [
                'stereocode/xslt/stereotype.xsl',
                'stereocode/xslt/remove_stereotypes.xsl'
            ]
        )
    ],
    scripts=['stereocode.py'],
    test_suite = '',
    # **extra

    license = "GPL",
    keywords = "static analysis stereotype stereocode srcML SDML",
    url = "www.sdml.com",
    long_description=read_docuemntation(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
    ],

)
# create_shortcut()