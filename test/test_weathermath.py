#!/usr/local/bin/python
# coding: utf-8

import sys

sys.path.insert(0, '../ventilation-control')

import unittest
import weathermath

# python -m unittest discover
class TestWeathermath(unittest.TestCase):

    def test_SDD(self):
        self.assertAlmostEqual( weathermath.SDD(20), 23.38, 2 )

    def test_DD(self):
        self.assertAlmostEqual( weathermath.DD(60, 20), 14.03, 2 )

    def test_AF(self):
        self.assertAlmostEqual( weathermath.AF(60, 20), 10.4, 1 )

