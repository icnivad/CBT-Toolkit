from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context, Template, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
import simplejson
from django.template import RequestContext
from models import  *
from django.conf import settings
from myforms import *
from registration.forms import RegistrationForm
import datetime

def thoughtView(request):
	if request.method=="POST":
		form=ThoughtForm(request.POST)
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
		return redirect(reverse('thought_distortion', kwargs={'thought_id':temp.pk}))
		
	else:
		form=ThoughtForm()
		c={'form':form}
		return render(request, "thought.html", c)

def detailView(request, thought_id):
	thought=Thought.objects.get(pk=thought_id)
	challenge=None
	try:
		challenge=Challenge.objects.get(thought=thought)
	except:
		pass
	c={'thought':thought, 'challenge':challenge}
	return render(request, "thought_detail.html", c)

def editView(request, thought_id):
	if request.method=="POST":
		thought=Thought.objects.get(pk=thought_id)
		form=ThoughtForm(request.POST, instance=thought)
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
		return HttpResponse("")
	else:
		thought=Thought.objects.get(pk=thought_id)
		form=ThoughtForm(instance=thought)
		c={'thought':thought, 'form':form}
		return render(request, "thought_edit.html", c)

def distortionView(request, thought_id, questions=True):
	thought=Thought.objects.get_with_permission(request.user, thought_id)
	form=DistortionForm(questions=questions, instance=thought)
	if request.method=="POST":
		form=DistortionForm(request.POST, instance=thought, questions=questions)
		if form.is_valid():
			form.save()
		else:
			print 'not valid'
			pass #trouble trouble trouble!
		return redirect(reverse('thought_challenge', kwargs={'thought_id':thought.pk}))
	else:		
		templateName="distortion.html"
		print form
		c={'thought':thought, 'form':form}
		return render(request, templateName, c)
	
def challengeView(request, thought_id):
	templateName="challenge.html"
	thought=Thought.objects.get_with_permission(request.user, thought_id)
	if thought==None:
		#Need to replace this with something real
		return redirect("oops")
	else:
		questions=thought.get_unanswered_questions()
		question=questions[0]
		print question
		form=ChallengeForm(initial={'challenge_question':question})
		c={'thought':thought, 'form':form, 'question':question}
		if request.method=="POST":
			form=ChallengeForm(request.POST)
			if form.is_valid():
				temp=form.save(commit=False)
				temp.thought=thought
				temp.user=request.user
				temp.save()
			else:
				pass
		return render(request, templateName, c)
	
def deleteView(request, thought_id):
	thought=Thought.objects.get_with_permission(request.user, pk=thought_id)
	if request.method=="POST":
		if ((request.user.is_authenticated()) and (request.user==thought.user)):
			thought.delete()
		else:
			pass
		return HttpResponse('deleted');
	else:
		c={'thought':thought}
		return render(request, "thought_delete.html", c)
	
def listView(request):
	thoughts=Thought.objects.filter(user=request.user).order_by('datetime')
	c={'thoughts':thoughts}
	return render(request, 'thought_list.html', c)