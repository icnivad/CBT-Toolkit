from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'mood_tracker.views.simple'),
)
