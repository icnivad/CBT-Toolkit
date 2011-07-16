from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context, Template
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
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
		logged_in=True
		username=request.user.username
		c={'logged_in':logged_in, 'username':username}
		c.update(csrf(request))
		return redirect("/thought")
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
				pass #account disabled
		else:
			pass #invalid login
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
		else:
			c={'logged_in':logged_in, 'username':username, 'loginform':LoginForm(), 'signupform':form}
			c.update(csrf(request))
			return render(request, "main.html", c)
				
def logoutView(request):
	logout(request)
	return redirect("/")

def deleteThought(request):
	if request.method=="POST":
		if request.user.is_authenticated():
			id=request.POST['id']
			action=request.POST['action']
			print id 
			print action
			thought=Thought.objects.get(pk=id)
			if action=="delete":
				thought.delete()
				thoughts=Thought.objects.all()
				return render(request, "thought_list.html", {'thoughts':thoughts})
	
def thoughtView(request):
	if request.method=="POST":
		form=ThoughtForm(request.POST)
		moodForm=MoodForm(request.POST)
		if form.is_valid():
			temp=form.save(commit=False)
			temp.user=request.user
			temp.save()
		else:
			print 'invalid'
		if moodForm.is_valid():
			temp=moodForm.save(commit=False)
			temp.user=request.user
			temp.save()
			return redirect("/thought")
		else:
			print 'invalid'
	else:
		form=ThoughtForm()
		moodForm=MoodForm()
		thoughts=Thought.objects.filter(user=request.user).order_by('datetime')
		logged_in=False
		username=""
		if request.user.is_authenticated():
			logged_in=True
			username=request.user.username
		c={'form':form, 'moodForm':moodForm, 'thoughts':thoughts, 'logged_in':logged_in, 'username':username}
		return render(request, "thought.html", c)

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
