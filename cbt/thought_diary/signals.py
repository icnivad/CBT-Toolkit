from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from registration.signals import user_registered
from models import Thought
from spreedly.pyspreedly.api import Client
import settings

@receiver(user_registered)
def lazy_signup(sender, **kwargs):
	request=kwargs['request']
	user=kwargs['user']
	
	#sign user up for free trial
	c=Client(settings.SPREEDLY_AUTH_TOKEN, settings.SPREEDLY_SITE_NAME)
	c.create_subscriber(user.pk, user.username)
	c.subscribe(user.pk, plan_id=settings.SPREEDLY_FREE_TRIAL_ID, trial=True)
	Thought.reparent_all_my_session_objects(request.session, user)
	
@receiver(user_logged_in)
def lazy_login(sender, **kwargs):
	request=kwargs['request']
	user=kwargs['user']
	print request
	if request.user.is_active:
		Thought.reparent_all_my_session_objects(request.session, user)