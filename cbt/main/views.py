from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context, Template, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.template import RequestContext
from models import  *
from django.conf import settings
from registration.forms import RegistrationForm
from myforms import ContactForm
from django.core.mail import send_mail


def mainView(request):
	if request.user.is_authenticated():
		return redirect(reverse('dashboard'))
	else:
		return render(request, "main.html")

def getLoginMessage(request):
	return render(request, "login_message.html")

def server_error(request, template_name='500.html'):
	"Always includes MEDIA_URL"
	from django.http import HttpResponseServerError
	t = loader.get_template(template_name)
	c=Context({'MEDIA_URL':settings.MEDIA_URL})
	c.update(csrf(request))
	return HttpResponseServerError(t.render(c))

def contentView(request, templateName):
	if templateName[-1]=="/":
		templateName=templateName[:-1]
	return render(request, templateName+".html")

def dashboardView(request):
	return render(request, "dashboard.html")
	
def contact(request):
	#If thanks is true - displays a thank you note
	form=ContactForm(request.POST or None)
	if request.method=="POST" and form.is_valid():	
		topic=form.cleaned_data['topic']
		message=form.cleaned_data['message']
		email=form.cleaned_data['email']
		try:
			send_mail("MoodToolkit - From:"+email+" Subject: "+topic, message, email, ['bearle2009@gmail.com'])
		# should log this exception!
		except Exception:
			error='Oops, there was a problem sending your email!  Please try again!'
			return render(request, 'contact.html', {'form':form, 'error':error})
		return redirect(reverse('thanks'))
	return render(request, 'contact.html', {'form':form})

def thanks(request):
	return render(request, 'thanks.html')
