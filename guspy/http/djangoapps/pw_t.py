import sys, os
INTERP = "/home/joran0420/packages/bin/python"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

def application(environ, start_response):
    import sys,os
    os.environ["PYTHONPATH"]="/home/joran0420/packages/lib/python2.7/site-libraries"
    sys.path.append('/home/joran0420/packages/lib/python2.7/site-packages/MySQL_python-1.2.3-py2.7-linux-x86_64.egg')
    path = '/home/joran0420/djangoapps/'
    if path not in sys.path:
        sys.path.append(path)
    from pyinfo import pyinfo
    output = pyinfo()
    start_response('200 OK', [('Content-type', 'text/html')])
    return [output]
    return ['Hello World!\n']

