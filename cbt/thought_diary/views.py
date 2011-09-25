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
from django_session_stashable import SessionStashable
from django.views.generic.list_detail import object_list

def thoughtView(request):
	if request.method=="POST":
		form=ThoughtForm(request.POST)
		temp=""
		if form.is_valid():
			if(form.cleaned_data['thought']!=""):
				temp=form.save(commit=False)
				temp.save(request)
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
	print thought.get_challenges()
	c={'thought':thought}
	return render(request, "thought_detail.html", c)

def editView(request, thought_id):
	if request.method=="POST":
		thought=Thought.objects.get_with_permission(request, pk=thought_id)
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
	thought=Thought.objects.get_with_permission(request, thought_id)
	form=DistortionForm(questions=questions, instance=thought)
	if request.method=="POST":
		form=DistortionForm(request.POST, instance=thought, questions=questions)
		if form.is_valid():
			temp=form.save(commit=False)
			temp.save(request)
			form.save_m2m()
		else:
			print 'not valid'
			pass #trouble trouble trouble!
		return redirect(reverse('thought_challenge', kwargs={'thought_id':thought.pk}))
	else:		
		templateName="distortion.html"
		print form
		c={'thought':thought, 'form':form}
		return render(request, templateName, c)

def challengeView(request, thought_id, challenge_question_id=None):
	templateName="challenge.html"
	thought=Thought.objects.get_with_permission(request, thought_id)
	if request.method=="POST":
		form=ChallengeForm(request.POST)
		if form.is_valid():
			temp=form.save(commit=False)
			temp.thought=thought
			temp.user=request.user
			if challenge_question_id!=None:
				question=ChallengeQuestion.objects.get(pk=challenge_question_id)
				temp.challenge_question=question
			temp.save()
			form.save_m2m()
			stashed=False
			if Thought.num_stashed_in_session(request.session):
				stashed=True
			c={'thought':thought, 'form':form, 'stashed':stashed}
			return render(request, "challenge_success.html", c)
				
	#If there's no thought - we're in trouble
	if thought==None:
		#Need to replace this with something real
		return redirect("oops")
	
	#Don't have a question to respond - no trouble - just get one.  
	#What do we do if all available questions have been answered though?
	elif challenge_question_id==None:
		questions=thought.get_unanswered_questions()
		if len(questions)==0:
			form=ChallengeForm()
			c={'thought':thought, 'form':form}
			return render(request, templateName, c)
		question=questions[0]
		return redirect(reverse('thought_challenge', kwargs={'thought_id':thought.pk, 'challenge_question_id':question.pk}))
	else:
		question=ChallengeQuestion.objects.get(pk=challenge_question_id)
		questions=thought.get_unanswered_questions()
		next_url=None
		try:
			i=questions.index(question)
			next=questions[i+1]
			next_url=reverse('thought_challenge', kwargs={'thought_id':thought.pk, 'challenge_question_id':next.pk})
		except:
			pass
		form=ChallengeForm(initial={'challenge_question':question})
		c={'thought':thought, 'form':form, 'question':question, 'next_url':next_url}
		return render(request, templateName, c)
	
def deleteView(request, thought_id):
	thought=Thought.objects.get_with_permission(request, thought_id)
	if request.method=="POST":
		thought.delete_with_permission(request)
		return HttpResponse('deleted');
	else:
		c={'thought':thought}
		return render(request, "modal_delete.html", c)
	
def listView(request):
	thoughts=Thought.objects.filter(created_by=request.user).order_by('-datetime')
	c={'thoughts':thoughts}
	return object_list(request, template_name='thought_list.html', queryset=thoughts, paginate_by=10)