from django.conf.urls.defaults import *
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from thought_diary.views import *
import settings
from thought_diary.models import Thought
from thought_diary.myforms import ThoughtForm
from django.contrib.auth.views import password_reset, password_reset_done, password_change, password_change_done
from django.views.generic.simple import direct_to_template
import spreedly.settings as spreedly_settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler500 = 'thought_diary.views.server_error'

#today we're playing with generic views
urlpatterns = patterns('',
    (r'^Media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.MEDIA_ROOT}),
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
    url(r'^content/(?P<templateName>.*)$', contentView, name='content'),
    # Example:
    # (r'^cbt/', include('cbt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.simple.urls')),
#    (r'', errorView),
    (r'^%s' % spreedly_settings.SPREEDLY_URL[1:], include('spreedly.urls')),
)

urlpatterns += patterns('',
  (r'^accounts/profile/$', direct_to_template, {'template': 'registration/profile.html'}),
  (r'^accounts/password_reset/$', password_reset, {'template_name': 'registration/password_reset.html'}),
  (r'^accounts/password_reset_done/$', password_reset_done, {'template_name': 'registration/password_reset_done.html'}),
  (r'^accounts/password_change/$', password_change, {'template_name': 'registration/password_change.html'}),
  (r'^accounts/password_change_done/$', password_change_done, {'template_name': 'registration/password_change_done.html'}),
)
