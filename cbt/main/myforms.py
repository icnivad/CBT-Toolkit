from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.utils.text import *

# A simple contact form with four fields.
class ContactForm(forms.Form):
	email = forms.EmailField()
	topic = forms.CharField()
	message = forms.CharField(widget=forms.Textarea())
	
	def send(self):
		send_mail("MoodToolkit: "+self.topic, self.message, self.email, ['bearle2009@gmail.com'])