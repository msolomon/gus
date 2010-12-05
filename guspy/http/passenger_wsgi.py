import sys, os

INTERP = "/home/joran0420/packages/bin/python"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+"gus/")
os.environ['DJANGO_SETTINGS_MODULE'] = "gus.settings"
import django.core.handlers.wsgi
from gus import *
application = django.core.handlers.wsgi.WSGIHandler()
