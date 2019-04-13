##
# @file test_stereotype_cppunit_xslt.py
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


import unittest, lxml.etree as et, lxml, os, os.path
from libstereocode import *
from testlib import *



class TestStereotypeXslt(unittest.TestCase):
    @srcMLifyCode("tests/test_data/api_utility_verifier.cpp")
    def test_api_utility_verifier(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 1,
            "functionInfo":
            [
                ("storeTest", ['command', 'collaborator', 'boolean_verifier', 'api_utility_verifier']),
                
            ]
        })


    @srcMLifyCode("tests/test_data/assertion_verifier.cpp")
    def test_assertion_verifier(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 1,
            "functionInfo":
            [
                ("ageTest", ['command', 'boolean_verifier', 'equality_verifier', 'doubles_equality_verifier', 'exception_verifier', 'no_exception_verifier', 'assertion_verifier', 'utility_verifier', 'hybrid_verifier', 'branch_verifier', 'iterative_verifier']),
                
            ]
        })

    @srcMLifyCode("tests/test_data/boolean_verifier.cpp")
    def test_boolean_verifier(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 5,
            "functionInfo":
            [
                ("testAccessors", ['command', 'collaborator', 'equality_verifier', 'public_field_verifier']),
                ("testEqualityOperators", ['command', 'collaborator', 'boolean_verifier', 'equality_verifier', 'hybrid_verifier']),
                ("testEquality", ['command', 'stateless', 'boolean_verifier']),
                ("example", ['command', 'stateless', 'boolean_verifier']),
                ("anotherExample", ['command', 'stateless', 'boolean_verifier']),
                
            ]
        })

    
    @srcMLifyCode("tests/test_data/branch_verifier.cpp")
    def test_branch_verifier(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 2,
            "functionInfo":
            [
                ("ageTest", ['command', 'boolean_verifier', 'equality_verifier', 'doubles_equality_verifier', 'exception_verifier', 'no_exception_verifier', 'assertion_verifier', 'utility_verifier', 'hybrid_verifier', 'branch_verifier']),
                ("load", ['command', 'collaborator', 'boolean_verifier', 'equality_verifier', 'hybrid_verifier', 'branch_verifier', 'api_utility_verifier', 'public_field_verifier']),

            ]
        })

    
    @srcMLifyCode("tests/test_data/doubles_equality_verifier.cpp")
    def test_doubles_equality_verifier(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 3,
            "functionInfo":
            [
                ("floatConstructorTest", ['command', 'collaborator', 'equality_verifier', 'doubles_equality_verifier', 'exception_verifier', 'no_exception_verifier', 'hybrid_verifier', 'public_field_verifier']),
                ("assignmentOperatorTest", ['command', 'collaborator', 'equality_verifier', 'doubles_equality_verifier', 'hybrid_verifier', 'public_field_verifier']),
                ("floatValueTest", ['command', 'doubles_equality_verifier']),
                
            ]
        })

    @srcMLifyCode("tests/test_data/equality_verifier.cpp")
    def test_equality_verifier(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 4,
            "functionInfo":
            [
                ("testAccessors", ['command', 'collaborator', 'equality_verifier', 'public_field_verifier']),
                ("testEqualityOperators", ['command', 'collaborator', 'boolean_verifier', 'equality_verifier', 'hybrid_verifier']),
                ("testRun", ['command', 'equality_verifier']),
                ("test_toString", ['command', 'equality_verifier']),
                
            ]
        })


    
    @srcMLifyCode("tests/test_data/exception_verifier.cpp")
    def test_exception_verifier(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 1,
            "functionInfo":
            [
                ("exceptionTest", ['command', 'exception_verifier']),
                
            ]
        })

    @srcMLifyCode("tests/test_data/execution_tester.cpp")
    def test_execution_tester(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 1,
            "functionInfo":
            [
                ("ageTest", ['set', 'collaborator', 'unclassified', 'execution_tester']),
                
            ]
        })


    @srcMLifyCode("tests/test_data/hybrid_verifier.cpp")
    def test_hybrid_verifier(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 2,
            "functionInfo":
            [
                ("equalTest", ['command', 'boolean_verifier', 'equality_verifier', 'hybrid_verifier']),
                ("testEquals", ['command', 'collaborator', 'boolean_verifier', 'equality_verifier', 'doubles_equality_verifier', 'hybrid_verifier']),
                
            ]
        })

    
    @srcMLifyCode("tests/test_data/iterative_verifier.cpp")
    def test_iterative_verifier(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 1,
            "functionInfo":
            [
                ("ageTest", ['command', 'boolean_verifier', 'equality_verifier', 'doubles_equality_verifier', 'exception_verifier', 'no_exception_verifier', 'assertion_verifier', 'utility_verifier', 'hybrid_verifier', 'branch_verifier', 'iterative_verifier']),
                
            ]
        })

    @srcMLifyCode("tests/test_data/public_field_verifier.cpp")
    def test_public_field_verifier(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 2,
            "functionInfo":
            [
                ("load", ['non-void-command', 'collaborator', 'boolean_verifier', 'equality_verifier', 'hybrid_verifier', 'api_utility_verifier', 'public_field_verifier']),
                ("assignmentOperatorTest", ['command', 'collaborator', 'equality_verifier', 'doubles_equality_verifier', 'hybrid_verifier', 'public_field_verifier']),
                
            ]
        })

    
    @srcMLifyCode("tests/test_data/test_cleaner.cpp")
    def test_test_cleaner(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 2,
            "functionInfo":
            [
                ("tearDown", ["test_cleaner"]),
                ("tearAddition", ['command', 'boolean_verifier']),
                 
            ]
        })


    @srcMLifyCode("tests/test_data/test_initializer.cpp")
    def test_test_initializer(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 2,
            "functionInfo":
            [
                ("setUp", ['command', 'test_initializer']),
                ("testEquality", ['command', 'boolean_verifier']),
                   
            ]
        })

    @srcMLifyCode("tests/test_data/utility_verifier.cpp")
    def test_utility_verifier(self, tree):
        executeAndTestTransform(self, tree, stereocodeDoc, {
            "matchesWithAStereotype": 2,
            "functionInfo":
            [
                ("ageTest", ['command', 'exception_verifier', 'no_exception_verifier', 'assertion_verifier', 'utility_verifier', 'hybrid_verifier', 'branch_verifier']),
                ("test_method", ['command', 'collaborator', 'boolean_verifier', 'utility_verifier', 'hybrid_verifier']),
                
            ]
        })