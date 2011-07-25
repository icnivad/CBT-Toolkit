from localsettings import *

#deal with urls
APPEND_SLASH=True

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.request',
'django.core.context_processors.auth',
'django.core.context_processors.debug',
'django.core.context_processors.i18n',
'thought_diary.context_processors.media_url',
)