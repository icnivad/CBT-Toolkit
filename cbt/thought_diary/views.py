from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context, Template
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
import simplejson
from django.views.generic import *
from django.views.generic.edit import *
from django.template import RequestContext
from models import  *
import settings
from myforms import *
import datetime

def mainView(request):
	logged_in=False
	username=""
	if request.user.is_authenticated():
		return redirect(reverse('thought'))
	else:
		loginForm=LoginForm()
		signupForm=CreateUserForm()
		c={'logged_in':logged_in, 'username':username, 'loginform':loginForm, 'signupform':signupForm}
		c.update(csrf(request))
		return render(request, "main.html", c)

def loginAction(request):
	if request.method=="POST":
		form=LoginForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user=authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect("/")
				else:
					pass
			else:
				errormsg="You have entered an incorrect username or password.  Please try again."  
				c={'form':form, 'errormsg':errormsg}
				c.update(csrf(request))
				return render(request, "login.html", c)
		else:
			pass
	else:
		form=LoginForm()
	c={'form':form}
	c.update(csrf(request))
	return render(request, "login.html", c)

def signupAction(request):
	if request.method=="POST":
		form=CreateUserForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			email=form.cleaned_data['email']
			user=User.objects.create_user(username=username, email=email, password=password) 
			user.save()
			createdUser=authenticate(username=username, password=password)
			login(request, createdUser)
			return redirect("/")
		else:
			c={'logged_in':False, 'username':"", 'loginform':LoginForm(), 'signupform':form}
			c.update(csrf(request))
			return render(request, "main.html", c)
				
def logoutView(request):
	logout(request)
	return redirect("/")

def thoughtView(request):
	if request.method=="POST":
		form=ThoughtForm(request.POST)
		if form.is_valid():
			temp=form.save(commit=False)
			temp.user=request.user
			temp.save()
		else:
			print 'invalid'
		newForm=ThoughtForm()
		thoughts=Thought.objects.filter(user=request.user).order_by('datetime')
		c={'form':newForm, 'recent_thought':temp, 'thoughts':thoughts}
		return render(request, "thought.html", c)
		
	else:
		form=ThoughtForm()
		thoughts=Thought.objects.filter(user=request.user).order_by('datetime')
		c={'form':form, 'thoughts':thoughts}
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


def challengeView(request, thought_id):
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
	if not thought.user==request.user:
		return redirect("/")
	else:
		form=ChallengeForm()
		c={'thought':thought, 'form':form}
		return render(request, "challenge.html", c)
	
def thoughtDeleteView(request, thought_id):
	thought=Thought.objects.get(pk=thought_id)
	if ((request.user.is_authenticated()) and (request.user==thought.user)):
		thought.delete()
	else:
		pass
	
def errorView(request):
	logged_in=False
	username=""
	if request.user.is_authenticated():
		logged_in=True
		username=request.user.username
		c={'logged_in':logged_in, 'username':username}
		c.update(csrf(request))
		return render(request, "error.html", c)
	else:
		loginForm=LoginForm()
		c={'logged_in':logged_in, 'username':username, 'loginform':loginForm}
		c.update(csrf(request))
		return render(request, "error.html", c)

def testView(request):
	test=reverse('main')
	c={'test':test}
	return render(request, 'test.html', c)
	
def getThoughts(request):
	thoughts=Thought.objects.filter(user=request.user).order_by('datetime')
	c={'thoughts':thoughts}
	return render(request, 'thought_list.html', c)