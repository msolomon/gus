import sys, os
INTERP = "/home/joran0420/packages/bin/python"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = "GUS.settings"
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
