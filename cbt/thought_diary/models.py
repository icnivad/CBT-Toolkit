from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from south.modelsinspector import add_introspection_rules

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),"helper_functions"))
import datetime
import datetime_helper
from custom_fields import SeparatedValuesField
# Create your models here.

add_introspection_rules([], ["^thought_diary\.models\.MultiSelectField"])


class MultiSelectFormField(forms.MultipleChoiceField):
	widget = forms.CheckboxSelectMultiple

	def __init__(self, *args, **kwargs):
		self.max_choices = kwargs.pop('max_choices', 0)
		super(MultiSelectFormField, self).__init__(*args, **kwargs)
	
	def clean(self, value):
		print value
		if not value and self.required:
			raise forms.ValidationError(self.error_messages['required'])
		if value and self.max_choices and len(value) > self.max_choices:
			raise forms.ValidationError('You must select a maximum of %s choice%s.' % (apnumber(self.max_choices), pluralize(self.max_choices)))
		return value

class MultiSelectField(models.Field):
	__metaclass__ = models.SubfieldBase

	def get_internal_type(self):
		return "CharField"

	def get_choices_default(self):
		return self.get_choices(include_blank=False)

	def _get_FIELD_display(self, field):
		value = getattr(self, field.attname)
		choicedict = dict(field.choices)

	def formfield(self, **kwargs):
		# don't call super, as that overrides default widget if it has choices
		defaults = {'required': not self.blank, 'label': self.verbose_name, 
				'help_text': self.help_text, 'choices':self.choices}
		if self.has_default():
			defaults['initial'] = self.get_default()
		defaults.update(kwargs)
		return MultiSelectFormField(**defaults)

	def get_db_prep_value(self, value):
		if isinstance(value, basestring):
			return value
		elif isinstance(value, list):
			return ",".join(value)

	def to_python(self, value):
		if isinstance(value, list):
			return value
		elif value==None:
			return ''
		return value.split(",")

	def value_to_string(self, obj):
		value = self._get_val_from_obj(obj)
		return self.get_db_prep_value(value)

	def validate(self, value, model_instance):
		return

	def contribute_to_class(self, cls, name):
		super(MultiSelectField, self).contribute_to_class(cls, name)
		if self.choices:
			func = lambda self, fieldname = name, choicedict = dict(self.choices):",".join([choicedict.get(value,value) for value in getattr(self,fieldname)])
			setattr(cls, 'get_%s_display' % self.name, func)
	
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
		return str(self.item)+": "+str(self.value)

class Thought(models.Model):
	share=models.BooleanField(default=False)
	category=models.CharField(blank=True, max_length=100)
	thought=models.TextField(blank=True)
	situation=models.TextField(blank=True)
	user=models.ForeignKey(User)
	datetime=models.DateTimeField('time', editable=False)
	distortions=models.ManyToManyField("Distortion", blank=True, null=True)
	challenge_questions_answered=models.ManyToManyField("ChallengeQuestion", blank=True, null=True)
	
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
			mood=Mood.objects.filter(user=self.user, datetime=self.datetime)[0]
			return mood
		except:
			return ""
	
	def get_challenge(self):
		try:
			challenge=Challenge.objects.get(thought=self)
			return challenge
		except:
			return ""
			
class Distortion(models.Model):
	distortion=models.CharField(max_length=100)
	question=models.TextField(blank=True)
	explanation=models.TextField(blank=True)
	how_to_respond=models.TextField(blank=True)
	example=models.TextField(blank=True)
		
	def __unicode__(self):
		return self.distortion

class ChallengeQuestion(models.Model):
	question=models.TextField()
	distortion=models.ManyToManyField("Distortion", related_name="challenge_questions")
	def __unicode__(self):
		return self.question

class Challenge(models.Model):
	thought=models.ForeignKey(Thought)
	challenge_question=models.ManyToManyField("ChallengeQuestion")
	response=models.TextField()
	def __unicode__(self):
		return self.response

class UserProfile(models.Model):
	user=models.ForeignKey(User, unique=True)
	startedTracking=models.BooleanField(default=False)
	
def create_user_profile(sender, instance, created, **kwargs):
	profile, new=UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
\