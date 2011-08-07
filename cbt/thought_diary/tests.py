from models import *
from django.core.urlresolvers import reverse
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from unittest import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)
	
class ViewsTest(TestCase):
	def test_thought_view(self):
		thought_view=reverse('thought')
		self.assertEqual(thought_view, '/thought/')