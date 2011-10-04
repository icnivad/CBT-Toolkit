import os, sys, site
from django.core.handlers.wsgi import WSGIHandler

DIRPATH=os.path.abspath(os.path.dirname(__file__))
site.addsitedir(DIRPATH+"../VE/python2.7/site-packages")

activate_this = os.path.expanduser(DIRPATH+"../VE/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

sys.path.append(DIRPATH)
sys.path.append(DIRPATH+"cbt")

os.environ['DJANGO_SETTINGS_MODULE'] = 'cbt.settings'
application = WSGIHandler()
