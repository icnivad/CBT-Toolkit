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
    url(r'^(?P<thought_id>\d.*)/challenge/(?P<challenge_question_id>\d.*)/$', challengeView, name='thought_challenge'),
    url(r'^(?P<thought_id>\d.*)/distortion/$', distortionView, name='thought_distortion'),
    url(r'^(?P<thought_id>\d.*)/distortion/simple$', distortionView, {'questions':False}, name='thought_distortion_simple'),
    url(r'^(?P<thought_id>\d+)/$', detailView, name='thought_detail'),
    url(r'^(?P<thought_id>\d+)/delete/$', deleteView, name='thought_delete'),
    url(r'^(?P<thought_id>\d+)/edit/$', editView, name='thought_edit'),
    url(r'^list/$', listView, name='thought_list'),
)