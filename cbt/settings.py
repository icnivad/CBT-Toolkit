from localsettings import *
# should define EMAIL_HOST and EMAIL_PORT

import os
import sys



#spreedly controls
#SPREEDLY_AUTH_TOKEN='03743ec2ed1546ef8ee91ed6ef5f64c04c86b518'
#SPREEDLY_SITE_NAME='cbttoolkit'
#SPREEDLY_FREE_TRIAL_ID=13483
#SITE_URL="http://www.cbttoolkit.com"
#SPREEDLY_ALLOWED_PATHS=["/media/", "/admin/", "/"]

#We really really need to organize this file - oh well
LOGIN_REDIRECT_URL="/dashboard"
REGISTER_REDIRECT_URL="/dashboard"

#deal with urls
APPEND_SLASH=True


# set up a dictionary of urls that can be accessed anywhere - good for static urls
NAMED_URLS={
	'tutorial':'/blog/tutorial',
	'distortions':'/blog/tutorial#distorted-thinking',
	'howto':'/blog/thought-diary-how-it-works',
}
if not PRODUCTION:
	for k in NAMED_URLS:
		NAMED_URLS[k]="http://www.moodtoolkit.com"+NAMED_URLS[k]

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.request',
'django.core.context_processors.auth',
'django.core.context_processors.debug',
'django.core.context_processors.i18n',
'thought_diary.context_processors.get_useful_constants',
'django_session_stashable.stashed_object_counts',
)

MYFILEPATH=os.path.dirname(os.path.dirname(__file__))+"/"

template_dir=MYFILEPATH+"Templates"
TEMPLATE_DIRS = (
	template_dir,
	template_dir+"/Thoughts",
	template_dir+"/tagging",
	template_dir+"/registration",
        template_dir+"/Spreedly",
	template_dir+"/Content",
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS':False, 
}

AUTHENTICATION_BACKENDS = (
  'django.contrib.auth.backends.ModelBackend',
  'lazysignup.backends.LazySignupBackend',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
#    'spreedly.middleware.SpreedlyMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS = (
    'tagging',
    'registration',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
     'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'thought_diary',
    'south',
    #'spreedly',
    'mytags',
    #'lazysignup',
    'debug_toolbar',
)
