from django import template
from django.core.urlresolvers import resolve
register=template.Library()
from lazysignup.utils import is_lazy_user

@register.simple_tag
def active(request, name):
	try:
		res_url=resolve(request.path)
		res_name=res_url.url_name
		if(name==res_name):	
			return "active"
		else:
			pass
	except:
		#should probably log this error somehow
		pass

@register.filter
def nonlazy(user):
	return (user.is_authenticated() and (not is_lazy_user(user)) )