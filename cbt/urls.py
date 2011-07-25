from django.conf.urls.defaults import *
from django.views.generic import *
from thought_diary.views import *
import settings
from thought_diary.models import Thought
from thought_diary.myforms import ThoughtForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

thought_info = {
	'queryset' : Thought.objects.all(),
	'template_name': 'thought_list.html',
}

#today we're playing with generic views
urlpatterns = patterns('',
    (r'^Media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.MEDIA_ROOT}),
    (r'^login$', loginAction),
    (r'^logout$', logoutView),
    (r'^signup$', signupAction),
    (r'^thought$', thoughtView),
    (r'^thought/(?P<id>\d.*)/challenge$', challengeView),
    (r'^$', mainView),
    # Example:
    # (r'^cbt/', include('cbt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin', include(admin.site.urls)),
    (r'', errorView),
)
