from django.conf.urls.defaults import *
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from thought_diary.views import *
import settings
from thought_diary.models import Thought
from thought_diary.myforms import ThoughtForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler500 = 'thought_diary.views.server_error'

#today we're playing with generic views
urlpatterns = patterns('',
    (r'^Media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.MEDIA_ROOT}),
    (r'^login$', loginAction),
    (r'^logout$', logoutView),
    (r'^signup$', signupAction),
    url(r'^thought/$', thoughtView, name='thought'),
    url(r'^thought/(?P<thought_id>\d.*)/challenge/$', challengeView, name='thought_challenge'),
    url(r'^thought/(?P<thought_id>\d+)/$', thoughtDetailView, name='thought_detail'),
    url(r'^thought/(?P<thought_id>\d+)/delete/$', thoughtDeleteView, name='thought_delete'),
    url(r'^thought/(?P<thought_id>\d+)/edit/$', thoughtEditView, name='thought_edit'),
    url(r'^thought/list/$', getThoughts, name='thought_list'),
    (r'^test/', testView),
    url(r'^$', mainView, name='main'),
    url(r'^about/', 'django.views.generic.simple.direct_to_template', {'template': 'about.html'}),
    (r'^getloginmsg/', getLoginMessage),
    # Example:
    # (r'^cbt/', include('cbt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
#    (r'', errorView),
)
