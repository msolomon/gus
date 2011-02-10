"""
Contains tests for the widget class
"""

from django.test import TestCase
from gus2.gus_widget.models import *

class CreateDestroyTest(TestCase):
    '''Create and destroy a generic widget'''
    def test(self):
        self.w = Widget()
        self.assertTrue(self.w is not None)
        del self.w
