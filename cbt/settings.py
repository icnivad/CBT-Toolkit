from localsettings import *
import os
import sys

#lets see if we can speed up testing
#if 'test' in sys.argv:
#	DATABASE_ENGINE='sqlite3'

#deal with urls
APPEND_SLASH=True

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.request',
'django.core.context_processors.auth',
'django.core.context_processors.debug',
'django.core.context_processors.i18n',
'thought_diary.context_processors.get_useful_constants',
)

MYFILEPATH=os.path.dirname(os.path.dirname(__file__))+"/"

TEMPLATE_DIRS = (
	MYFILEPATH+"Templates/",
	MYFILEPATH+"Templates/Thoughts",
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
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
)
