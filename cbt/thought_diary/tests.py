from models import *
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from django.conf import settings

"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

class ModelTest(TestCase):
	fixtures=['test.json']
	def test_thought(self):
		thoughts=Thought.objects.all()
		for thought in thoughts:
			print thought.pk
		thought=Thought.objects.get(pk=2)
		self.assertEqual(thought.user.pk, 1)
	
	def test_user(self):
		for user in User.objects.all():
			print user.username

class ViewTest(TestCase):
	fixtures=['test.json']
	def setUp(self):
		self.client=Client()

	def test_thought_view(self):
		thought_view=reverse('thought')
		self.assertEqual(thought_view, '/thought/')
		
		test=self.client.login(username="ben", password="cold")	
		resp=self.client.get(thought_view)
		self.assertEqual(resp.status_code, 200)

	def test_challenge_view(self):
		challenge_view=reverse('thought_challenge', args=[2])
		self.assertEqual(challenge_view, '/thought/2/challenge/')
		
		#check if we can get a challenge view that does exist
		self.client.login(username="ben", password="cold")
		
		#check what happens if challenge doesn't exist
		not_exist_challenge_view=reverse('thought_challenge', args=[10000])
		resp=self.client.get(not_exist_challenge_view)