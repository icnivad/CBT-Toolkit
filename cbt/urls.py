from django.conf.urls.defaults import *
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from main.views import *
import settings
from django.contrib.auth.views import password_reset, password_reset_done, password_change, password_change_done
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler500 = 'thought_diary.views.server_error'

#today we're playing with generic views
urlpatterns = patterns('',
    (r'^Media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.MEDIA_ROOT}),
    url(r'^dashboard/$', dashboardView, name='dashboard'),
    url(r'^$', mainView, name='main'),
    url(r'^tryit/', tryView, name="try_it"),
    url(r'^about/', 'django.views.generic.simple.direct_to_template', {'template': 'about.html'}, name="about"),
    (r'^getloginmsg/', getLoginMessage),
    url(r'^content/(?P<templateName>.*)$', contentView, name='content'),
    (r'^thought/', include('thought_diary.urls')),
    (r'^mood/', include('mood_tracker.urls')),
    (r'^activity/', include('activity_planner.urls')),

    # Example:
    # (r'^cbt/', include('cbt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    url(r'^accounts/register/', 'registration.views.register', {'backend':'registration.backends.simple.SimpleBackend', 'success_url': settings.REGISTER_REDIRECT_URL}, name='register'),
    url(r'^accounts/login/', 'django.contrib.auth.views.login', name="login"),    
    (r'^accounts/', include('registration.backends.simple.urls')),

#    (r'', errorView),
#    (r'^%s' % spreedly_settings.SPREEDLY_URL[1:], include('spreedly.urls')),
)

urlpatterns += patterns('',
  (r'^accounts/profile/$', direct_to_template, {'template': 'registration/profile.html'}),
  (r'^accounts/password_reset/$', password_reset, {'template_name': 'registration/password_reset.html'}),
  (r'^accounts/password_reset_done/$', password_reset_done, {'template_name': 'registration/password_reset_done.html'}),
  (r'^accounts/password_change/$', password_change, {'template_name': 'registration/password_change.html'}),
  (r'^accounts/password_change_done/$', password_change_done, {'template_name': 'registration/password_change_done.html'}),
)
