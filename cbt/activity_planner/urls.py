from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'activity_planner.views.simple'),
)