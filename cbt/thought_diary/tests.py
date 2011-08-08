from models import *
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from django.conf import settings

print settings.DATABASE_ENGINE
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
	def setUp(self):
		self.client=Client()
		
		#create a user to test out - we should probably move this to fixtures soon
		user=User.objects.create_user(username="test", email="test@test.com", password="test")	
		user.save()

	def test_thought_view(self):
		thought_view=reverse('thought')
		self.assertEqual(thought_view, '/thought/')
	
		self.client.login(username="test", password="test")	
		resp=self.client.get(thought_view)
		self.assertEqual(resp.status_code, 200)

		
