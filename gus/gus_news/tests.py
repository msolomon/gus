from django.test import TestCase
from time import localtime, strftime
import unittest

class test_gus_news(TestCase):
    def setUp(self):
        self.failIfEqual(0, 1, "CANNOT TEST UI ELEMENTS")
