##
# @file test_stereotype_xslt.py
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


import unittest, lxml.etree as et, lxml
from stereocode import *
from testlib import *

class TestStereotypeXslt(unittest.TestCase):
    @srcMLifyCode("tests/test_data/stereotype/get.cpp")
    def test_basicXslt(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype":2,
            "functionInfo":
            [
                ("match1", ["get", "collaborator"]),
                ("match2", ["nonconstget"])
            ]
        })

    @srcMLifyCode("tests/test_data/stereotype/command.cpp")
    def test_commandTest(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 4,
            "functionInfo":
            [
                ("sort", ["command", "stateless"]),
                ("f", ["command"]),
                ("f2", ["stateless"]),
                ("f3", ["command"]),
            ]
        })

    @srcMLifyCode("tests/test_data/stereotype/empty.cpp")
    def test_empty(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 7,
            "functionInfo":
            [
                ("n1", ["collaborator", "empty"]),
                ("n2", ["collaborator", "empty"]),
                ("n3", ["collaborator", "empty"]),
                ("n5", ["collaborator", "empty"]),
                ("n6", ["empty"]),
                ("n7", ["empty"]),
                ("n8", ["empty"]),
            ]
        })


    @srcMLifyCode("tests/test_data/stereotype/command-collaborator.cpp")
    def test_empty(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 2,
            "functionInfo":
            [
                ("findWhite", ["unclassified"]),
                ("findWhite", ["unclassified"]),
             
            ]
        })