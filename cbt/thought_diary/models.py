from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from south.modelsinspector import add_introspection_rules
from django_session_stashable import SessionStashable

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
	created_by=models.ForeignKey(User, blank=True, null=True)
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
	created_by=models.ForeignKey(User, blank=True, null=True)
	item=models.CharField(blank=True, max_length=100)
	def __unicode__(self):
		return str(self.item)


class TrackItemStatus(models.Model):	
	datetime=models.DateTimeField('time')
	created_by=models.ForeignKey(User, blank=True, null=True)
	item=models.ForeignKey('TrackItem')
	value=models.NullBooleanField(blank=True, null=True)
	def __unicode__(self):
		return str(self.item)+": "+str(self.value)

class ThoughtManager(models.Manager):
	#returns either a thought that the user has permission to access or None
	def get_with_permission(self, request, thought_id):
		thought=self.get(pk=thought_id)
		if ((thought.created_by==request.user) or (thought.stashed_in_session(request.session))):
			return thought
		return None

	def latest_with_permission(self, request):
		if Thought.num_stashed_in_session(request.session):
			thoughts=Thought.get_stashed_in_session(request.session)
			return thoughts.order_by('-datetime')[0]
		elif request.user.is_active:
			return self.latest('datetime')

	def all_with_permission(self, request):
		thoughts=Thought.get_stashed_in_session(request.session)
		if request.user.is_active:
			thoughts=thoughts | self.filter(created_by=request.user)
		return thoughts.order_by('-datetime')

class Thought(models.Model, SessionStashable):
	share=models.BooleanField(default=False)
	category=models.CharField(blank=True, max_length=100)
	thought=models.TextField(blank=True)
	situation=models.TextField(blank=True)

	#stores user who created thought
	created_by=models.ForeignKey(User, blank=True, null=True)
	session_variable='thought_stash'
	context_count_name='thought_stash_count'

	datetime=models.DateTimeField('time', editable=False)
	distortions=models.ManyToManyField("Distortion", blank=True, null=True)
	objects=ThoughtManager()
	
	def delete_with_permission(self, request):
		if (request.user.is_authenticated() and (self.created_by==request.user)):
			super(Thought, self).delete()
		elif self.stashed_in_session(request.session):
			self.remove_from_session(request.session)
			
	#need to really check this method out to make sure its okay!
	def remove_from_session(self, session):
		if self.pk in session[self.session_variable]:
			session[self.session_variable].remove(self.pk)
			session.modified=True
			
	def save(self, request):
		if not self.datetime:
			self.datetime=datetime.datetime.now()
		if request.user.is_active:
			self.created_by=request.user			
			super(Thought, self).save()
		else:
			super(Thought, self).save()
			self.stash_in_session(request.session)
			
	def __unicode__(self):
		return self.thought
	
	def pretty_date(self):
		return datetime_helper.pretty_date(self.datetime)
	
	def get_challenges(self):
		return Challenge.objects.filter(thought=self)
	
	#includes answered and unanswered - but only for the distortions appropriate to this thought
	def get_all_questions(self):
		questions=[q for d in self.distortions.all() for q in d.challenge_questions.all()]
		questions.extend(ChallengeQuestion.objects.get_general_questions())
		return questions
		
	#definitely want to test these methods!
	def get_unanswered_questions(self):
		questions=self.get_all_questions()
		answered=[c.challenge_question for c in self.get_challenges()]
		left_questions=[q for q in questions if (q not in answered)]
		return left_questions
		
class Distortion(models.Model):
	distortion=models.CharField(max_length=100)
	question=models.TextField(blank=True)
	explanation=models.TextField(blank=True)
	how_to_respond=models.TextField(blank=True)
	example=models.TextField(blank=True)
		
	def __unicode__(self):
		return self.distortion

class ChallengeQuestionManager(models.Manager):
	def get_general_questions(self):
		questions=self.all()
		return [q for q in questions if (len(q.distortion.all())==0)]

class ChallengeQuestion(models.Model):
	question=models.TextField()
	distortion=models.ManyToManyField("Distortion", related_name="challenge_questions", blank=True, null=True)
	objects=ChallengeQuestionManager()
	
	def __unicode__(self):
		if len(self.distortion.all())>0:
			distortions=", ".join([d.distortion for d in self.distortion.all()])
			return distortions+": "+self.question
		else:
			return self.question
class ChallengeManager(models.Manager):
	def get_with_permission(self, request, response_id):
		challenge=self.get(pk=response_id)
		if ((challenge.thought.created_by==request.user) or (challenge.thought.stashed_in_session(request.session))):
			return challenge
		return None

class Challenge(models.Model):
	thought=models.ForeignKey(Thought)
	challenge_question=models.ForeignKey("ChallengeQuestion", blank=True, null=True)
	response=models.TextField()
	objects=ChallengeManager()
	def __unicode__(self):
		return self.response		
	
class UserProfile(models.Model):
	user=models.ForeignKey(User, unique=True)
	startedTracking=models.BooleanField(default=False)
	
def create_user_profile(sender, instance, created, **kwargs):
	profile, new=UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
\
