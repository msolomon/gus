import sys, os
INTERP = "/home/joran0420/packages/bin/python"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)
os.environ["PYTHONPATH"]="/home/joran0420/packages/lib/python2.7/site-libraries"

cwd = os.getcwd()
myapp_directory = cwd + '/GUS'
sys.stdout = sys.stderr
sys.path.insert(0,"/home/joran0420/djangoapps/GUS")
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'GUS.settings'
import django.core.handlers.wsgi
from paste.exceptions.errormiddleware import ErrorMiddleware
application = django.core.handlers.wsgi.WSGIHandler()
# To cut django out of the loop, comment the above application = ... line ,
# and remove "test" from the below function definition.
def testapplication(environ, start_response):
   status = '200 OK'
   output = 'Hello World! Running Python version ' + sys.version + '\n\n'
   response_headers = [('Content-type', 'text/plain'),
                       ('Content-Length', str(len(output)))]
   # to test paste's error catching prowess, uncomment the following line
   # while this function is the "application"
   #raise("error")
   start_response(status, response_headers)    
   return [output]
application = ErrorMiddleware(application, debug=True)


#import sys, os
#sys.path.insert(1, "/home/joran0420/djangoapps/")


#os.environ['DJANGO_SETTINGS_MODULE'] = "GUS1.settings"
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
