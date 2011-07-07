from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User
from django.forms import ModelForm
from models import *

class PasswordField(forms.CharField):
	widget=PasswordInput()
	required=True
	label="Enter Password: "

class CreateUserForm(forms.Form):
	username=forms.CharField(max_length=20, required=True)
	password=PasswordField()
	retype_password=PasswordField(label="Reenter Password")
	email=forms.CharField(required=False)
	
	def clean(self):
		cleaned=self.cleaned_data
		username=cleaned.get("username")
		exists=User.objects.filter(username=username)
		if exists:
			raise forms.ValidationError("Username not available.  Please try another.")
		pword=cleaned.get("password")
		rpword=cleaned.get("retype_password")
		if pword!=rpword:
			raise forms.ValidationError("Password does not match.")
		return cleaned
	
	def save(self, username, email, password):
		user=User.objects.create_user(username, email, password)
		user.save()

class LoginForm(forms.Form):
	username=forms.CharField(max_length=20, required=True)
	password=PasswordField()

class ThoughtForm(ModelForm):
	class Meta:
		model=Thought
		exclude=('user', 'datetime', 'share', 'issue')
		widgets={
			'thought':forms.Textarea(attrs={'class':'text_field'}),
			'situation':forms.Textarea(attrs={'class':'text_field'}),
		}
		
class MoodForm(ModelForm):
	class Meta:
		model=Mood
		exclude=('user', 'datetime')
