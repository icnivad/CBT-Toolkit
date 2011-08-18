from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context, Template, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
import simplejson
from django.views.generic import *
from django.views.generic.edit import *
from django.template import RequestContext
from models import  *
from django.conf import settings
from myforms import *
from registration.forms import RegistrationForm
import datetime

def mainView(request):
	if request.user.is_authenticated():
		return redirect(reverse('thought'))
	else:
		form=RegistrationForm()
		c={'form':form}
		c.update(csrf(request))
		return render(request, "main.html", c)

def thoughtView(request):
	if request.method=="POST":
		form=ThoughtForm(request.POST)
		moodForm=MoodForm(request.POST)
		temp=""
		if form.is_valid():
			if(form.cleaned_data['thought']!=""):
				temp=form.save(commit=False)
				temp.user=request.user
				temp.save()
			else:
				pass
		else:
			raise Exception('thought form invalid')
		if moodForm.is_valid():
			if ((moodForm.cleaned_data['mood'] is not None) or (moodForm.cleaned_data['feeling']!="")):
				mtemp=moodForm.save(commit=False)
				mtemp.user=request.user
				mtemp.save()
			else:
				pass
		else:
			raise Exception('mood form invalid')
		c={'recent_thought':temp}
		return render(request, "thought_message.html", c)
		
	else:
		form=ThoughtForm()
		moodForm=MoodForm()
		thoughts=Thought.objects.filter(user=request.user).order_by('datetime')
		c={'form':form, 'thoughts':thoughts, 'mood':moodForm}
		return render(request, "thought.html", c)

def thoughtDetailView(request, thought_id):
	thought=Thought.objects.get(pk=thought_id)
	challenge=None
	try:
		challenge=Challenge.objects.get(thought=thought)
	except:
		pass
	c={'thought':thought, 'challenge':challenge}
	return render(request, "thought_detail.html", c)

def thoughtEditView(request, thought_id):
	if request.method=="POST":
		thought=Thought.objects.get(pk=thought_id)
		form=ThoughtForm(request.POST, instance=thought)
		try:
			moodForm=MoodForm(request.POST, instance=thought.get_mood())
		except:
			moodForm=MoodForm(request.POST)
		temp=""
		if form.is_valid():
			if(form.cleaned_data['thought']!=""):
				temp=form.save(commit=False)
				temp.user=request.user
				temp.save()
			else:
				pass
		else:
			raise Exception('thought form invalid')
		if moodForm.is_valid():
			if ((moodForm.cleaned_data['mood'] is not None) or (moodForm.cleaned_data['feeling']!="")):
				mtemp=moodForm.save(commit=False)
				mtemp.user=request.user
				mtemp.save()
			else:
				pass
		else:
			raise Exception('mood form invalid')
		return HttpResponse("")
	else:
		thought=Thought.objects.get(pk=thought_id)
		form=ThoughtForm(instance=thought)
		try:
			moodForm=MoodForm(instance=thought.get_mood())
		except:
			moodForm=MoodForm()
		c={'thought':thought, 'form':form, 'mood':moodForm}
		return render(request, "thought_edit.html", c)

def challengeView(request, thought_id):
	templateName="challenge_thought_form.html"
	errors=False
	error_msg=""
	form=ChallengeForm()
	thought=""
	try:
		thought=Thought.objects.get(pk=thought_id)
		if request.method=="POST":
			form=ChallengeForm(request.POST)
			if form.is_valid():
				temp=form.save(commit=False)
				temp.thought=thought
				temp.user=request.user
				temp.save()
			else:
				pass
			return HttpResponse("success")
		else:
			if not thought.user==request.user:
				#need to write this so it returns an error_msg - can't access thought
				errors=True
				thought=""
				error_msg="Uh oh, it looks like you don't have permission to access this thought."
				form=""
			else:
				pass
	except: 
		thought=""
		errors=True
		error_msg="Uh oh, it looks like that thought does not exist!  Our bad!"
		form=""
	c={'thought':thought, 'form':form, 'errors':errors, 'error_msg':error_msg}
	return render(request, templateName, c)
	
def thoughtDeleteView(request, thought_id):
	thought=Thought.objects.get(pk=thought_id)
	if request.method=="POST":
		if ((request.user.is_authenticated()) and (request.user==thought.user)):
			thought.delete()
		else:
			pass
		return HttpResponse('deleted');
	else:
		c={'thought':thought}
		return render(request, "thought_delete.html", c)

def testView(request):
	test=reverse('main')
	c={'test':test}
	return render(request, 'test.html', c)
	
def getThoughts(request):
	thoughts=Thought.objects.filter(user=request.user).order_by('datetime')
	c={'thoughts':thoughts}
	return render(request, 'thought_list.html', c)

def getLoginMessage(request):
	return render(request, "login_message.html")
	
def server_error(request, template_name='500.html'):
	"Always includes MEDIA_URL"
	from django.http import HttpResponseServerError
	t = loader.get_template(template_name)
	c=Context({'MEDIA_URL':settings.MEDIA_URL})
	c.update(csrf(request))
	return HttpResponseServerError(t.render(c))

