import os
import sys

from django.core.handlers.wsgi import WSGIHandler

sys.path.append("/home/tukipenda/webapps/cbt/CBT-Toolkit")
sys.path.append("/home/tukipenda/webapps/cbt/CBT-Toolkit/cbt")

os.environ['DJANGO_SETTINGS_MODULE'] = 'cbt.settings'
application = WSGIHandler()
