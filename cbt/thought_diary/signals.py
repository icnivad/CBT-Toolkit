from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from registration.signals import user_registered
from models import Thought
import settings

@receiver(user_registered)
def lazy_signup(sender, **kwargs):
	request=kwargs['request']
	user=kwargs['user']
	Thought.reparent_all_my_session_objects(request.session, user)
	
@receiver(user_logged_in)
def lazy_login(sender, **kwargs):
	request=kwargs['request']
	user=kwargs['user']
	print request
	if request.user.is_active:
		Thought.reparent_all_my_session_objects(request.session, user)
