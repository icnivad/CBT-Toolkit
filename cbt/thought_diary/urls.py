from django.conf.urls.defaults import *
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from views import *
from models import Thought
from myforms import ThoughtForm
from django.views.generic.simple import direct_to_template

#today we're playing with generic views
urlpatterns = patterns('',
    url(r'^$', thoughtView, name='thought'),
    url(r'^(?P<thought_id>\d.*)/challenge/$', challengeView, name='thought_challenge'),
    url(r'^(?P<thought_id>\d+)/$', thoughtDetailView, name='thought_detail'),
    url(r'^(?P<thought_id>\d+)/delete/$', thoughtDeleteView, name='thought_delete'),
    url(r'^(?P<thought_id>\d+)/edit/$', thoughtEditView, name='thought_edit'),
    url(r'^list/$', getThoughts, name='thought_list'),
)