from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),"helper_functions"))
import datetime
import datetime_helper
from custom_fields import SeparatedValuesField
# Create your models here.

class Mood(models.Model):
	feeling=models.CharField(blank=True, max_length=100)
	mood=models.IntegerField(blank=True, null=True)
	user=models.ForeignKey(User)
	datetime=models.DateTimeField('time')
	def save(self):
		if not self.datetime:
			self.datetime=datetime.datetime.now()
		super(Mood, self).save()
		
	def __unicode__(self):
		return str(self.mood)
	
	def pretty_date(self):
		return datetime_helper.pretty_date(self.datetime)
	
class TrackItem(models.Model):
	user=models.ForeignKey(User)
	item=models.CharField(blank=True, max_length=100)
	def __unicode__(self):
		return str(self.item)


class TrackItemStatus(models.Model):	
	datetime=models.DateTimeField('time')
	user=models.ForeignKey(User)
	item=models.ForeignKey('TrackItem')
	value=models.NullBooleanField(blank=True, null=True)
	def __unicode__(self):
		return str(self.item+": "+str(self.value))


class Thought(models.Model):
	THOUGHT_CHOICES=(
		("1", "Mental Filter"),
		("2", "Judgements"),
		("3", "Mind-Reading"),
		("4", "Emotional Reasoning"),
		("5", "Prediction"),
		("6", "Comparisons"),
		("7", "Mountains and Molehills"),
		("8", "Catastrophizing"),
		("9", "Critical Self"),
		("10", "Black and White Thinking"),
		("11", "Shoulds and Musts"),
		("12", "Memories"),
	)
	CATEGORY_CHOICES=(
		("1", "Family"),
		("2", "Relationships"),
		("3", "Work"),
		("4", "Friends"),
		("5", "Pleasure"),
		("6", "Travel"),
		("7", "Health"),
		("8", "Kids"),
		("9", "Money"),
		("10","Self"),
		("11", "Chores"),
		("12", "Other")

	)
	share=models.BooleanField(default=False)
	category=models.CharField(blank=True, max_length=100, choices=CATEGORY_CHOICES)
	thought=models.TextField(blank=True)
	situation=models.TextField(blank=True)
	note=models.TextField(blank=True)
	coping=models.TextField(blank=True)
	user=models.ForeignKey(User)
	datetime=models.DateTimeField('time', editable=False)
	distortion=models.CharField(blank=True, max_length=100, choices=THOUGHT_CHOICES)
	
	def save(self):
		if not self.datetime:
			self.datetime=datetime.datetime.now()
		super(Thought, self).save()
		
	def __unicode__(self):
		return self.thought
	
	def pretty_date(self):
		return datetime_helper.pretty_date(self.datetime)
		
	def get_mood(self):
		try:
			mood=Mood.objects.filter(datetime=self.datetime)[0]
			return mood
		except:
			return ""
			
class UserProfile(models.Model):
	user=models.ForeignKey(User, unique=True)
	startedTracking=models.BooleanField(default=False)
	
def create_user_profile(sender, instance, created, **kwargs):
	profile, new=UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)