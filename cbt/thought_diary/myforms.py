from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.models import ModelMultipleChoiceField
from django.core.validators import validate_email
from django.utils.text import *
from models import *


class ThoughtForm(ModelForm):
	class Meta:
		model=Thought
		fields=('thought', 'situation', 'category')
		widgets={
			'thought':forms.Textarea(attrs={'class':'text_field'}),
			'situation':forms.Textarea(attrs={'class':'text_field'}),			
			'category':forms.TextInput(attrs={'class':'text_field'}),
		}
		
class ChallengeForm(ModelForm):
	class Meta:
		model=Challenge
		exclude=('thought', 'distortion', 'challenge_question')
		widgets={
			'response':forms.Textarea(attrs={'class':'text_field'}),
		}

class DistortionCustomDisplay(ModelMultipleChoiceField):
	def __init__(self, *args, **kwargs):
		self.questions=kwargs.pop('questions')
		ModelMultipleChoiceField.__init__(self, *args, **kwargs)
	
	def label_from_instance(self, obj):
		if self.questions:
			return obj.question
		else:
			return obj.distortion

class DistortionForm(ModelForm):
	def __init__(self, *args, **kwargs):
		questions=kwargs.pop('questions')
		super(DistortionForm, self).__init__(*args, **kwargs)
		self.fields['distortions']=DistortionCustomDisplay(queryset=Distortion.objects.all(), widget=forms.CheckboxSelectMultiple, questions=questions, required=False)

	class Meta:
		model=Thought
		fields=('distortions',)

class MoodForm(ModelForm):
	class Meta:
		model=Mood
		exclude=('user', 'datetime')
		widgets={
			'mood':forms.TextInput(attrs={'class':'text_field'}),
			'feeling':forms.TextInput(attrs={'class':'text_field'}),
		}
