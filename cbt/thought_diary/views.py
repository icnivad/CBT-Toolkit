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
		return render(request, "dashboard.html", c)
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
			pass
		else:
			pass #not valid signup
		
def logoutView(request):
	logout(request)
	return render(request, "logout.html")

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

def chartView(request):
	mood_data=""
	logged_in=False
	username=""
	if request.user.is_authenticated():
		logged_in=True
		username=request.user.username
	return render(request, "mood_chart.html", {'logged_in':logged_in, 'username':username})

def moodData(request):
	moods=Mood.objects.all()
	moodData=[]
	for mood in moods:
		moodData.append([mood.datetime.strftime('%Y-%m-%d %I%p'), mood.mood])
	return HttpResponse(simplejson.dumps(moodData))
	
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
		thoughts=Thought.objects.order_by('datetime')
		logged_in=False
		username=""
		if request.user.is_authenticated():
			logged_in=True
			username=request.user.username
		c={'form':form, 'moodForm':moodForm, 'thoughts':thoughts, 'logged_in':logged_in, 'username':username}
		return render(request, "thought.html", c)

def trackView(request):
	if request.method=="POST":
		for key, value in request.POST.iteritems():
			if key.startswith("item"):
				key=int(key.split(":")[1])
				item=TrackItem.objects.get(pk=key)
				dt=datetime.datetime.now()
				if value=="yes":
					itemstatus=TrackItemStatus(user=request.user, item=item, value=True, datetime=dt)
				elif value=="no":
					itemstatus=TrackItemStatus(user=request.user, item=item, value=False, datetime=dt)
				else:
					itemstatus=TrackItemStatus(user=request.user, item=item, datetime=dt)
				itemstatus.save()
	else:
		logged_in=False
		username=""
		items=[]
		if request.user.is_authenticated():
			logged_in=True
			username=request.user.username
			c={'logged_in':logged_in, 'username':username, 'items':items}
			c.update(csrf(request))
			if request.user.get_profile().startedTracking==False:
				return redirect("/track/new")
			else:
				items=TrackItem.objects.filter(user=request.user)
				c.update({'items':items})
				return render(request, "track_mood.html", c)

def newTrackView(request):
	if request.method=="POST":
		for i in [1, 2, 3, 4, 5]:
			try:
				itemString=request.POST['item'+str(i)]
				if itemString!="":
					nitem=TrackItem(user=request.user, item=itemString)
					nitem.save()
					print nitem
			except:
				pass
		profile=request.user.get_profile()
		profile.startedTracking=True
		profile.save()
	else:
		logged_in=False
		username=""
		if request.user.is_authenticated():
			logged_in=True
			username=request.user.username
		c={'logged_in':logged_in, 'username':username}
		c.update(csrf(request))
		return render(request, "track_mood_first.html", c)
	
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
