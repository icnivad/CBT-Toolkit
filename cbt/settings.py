from localsettings import *
import os

#deal with urls
APPEND_SLASH=True

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.request',
'django.core.context_processors.auth',
'django.core.context_processors.debug',
'django.core.context_processors.i18n',
'thought_diary.context_processors.media_url',
)

MYFILEPATH=os.path.dirname(os.path.dirname(__file__))+"/"

TEMPLATE_DIRS = (
	MYFILEPATH+"Templates/",
	MYFILEPATH+"Templates/Thoughts",
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)