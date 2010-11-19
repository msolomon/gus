#!/usr/bin/python
 #{{pastelbox | background=#efdfff | content=This page looks weird because it's actually a script used by the [[Django]] setup. Go look at that instead! }}<pre>
import sys, os, urllib2, imp, signal, re

def missing(m):
    if sys.executable == "/usr/bin/python":
        print "Uh-oh, it looks like your server doesn't have %s installed." % m
        print "Ask DreamHost Support to install it for you!"
    else:
        print "It looks like you're using a nonstandard Python install which doesn't"
        print "have %s installed. You will need to revert to the system's default" % m
        print "Python install (or install %s manually) to use this script." % m
    print
    print "[ Executable: %s ]" % sys.executable
    sys.exit(1)

try:
    import django
except ImportError:
    missing("django")

try:
    import MySQLdb
except ImportError:
    missing("MySQLdb")

try:
    import readline
except:
    pass # we can live without readline!

if not os.path.isdir("public"):
    print "Either you aren't in the proper directory for your domain, or"
    print "your domain isn't set to use Passenger. Check the instructions"
    print "on the Wiki at:"
    print
    print "   http://wiki.dreamhost.com/Django"
    print
    print "for details."
    sys.exit(1)

if os.path.exists("passenger_wsgi.py"):
    print "It looks like this domain has already been set up to use Django!"
    print "If it hasn't, remove the passenger_wsgi.py file and try again."
    sys.exit(1)

domain = None
for chunk in os.getcwd().split(os.path.sep)[::-1]:
    if '.' not in chunk: continue
    domain = chunk
    break

if domain is None:
    print "Hrm, I can't figure out what the domain name for this directory is."
    print "What is it?"
    domain = raw_input(">> ").strip()
    print "Thanks!"
    print
else:
    print "Looks like your domain is probably %s ... cool." % domain

print "Testing domain service... ",

cookie = "django-%d" % os.getpid()
f = open("public/django-setup-test.txt", "w")
f.write(cookie)
f.close()

if urllib2.urlopen("http://%s/django-setup-test.txt" % domain).read() != cookie:
    print "failed!"
    print "Either your domain isn't resolving properly, or something"
    print "strange is keeping me from loading a file from it. You'll"
    print "need to fix that before you can continue."
    sys.exit(1)

os.unlink("public/django-setup-test.txt")

print "lookin' good"

while True:
    print
    print "What would you like to name your project?"
    projname = raw_input(">> ").strip()
    if not projname.replace("_", "").isalnum() or projname[0].isdigit():
        print "That isn't a valid name -- your project's name must be a valid"
        print "Python module name. (It can't contain spaces, for instance.)"
        continue
    try:
        imp.find_module(projname)
        print "That name is already used by a Python module."
        print "Try something more specific!"
    except ImportError:
        print "An excellent name!"
        break

print
print
print "You'll need a database for your Django project. If you don't already"
print "have one ready, you can create one from the DreamHost Panel at:"
print
print "  https://panel.dreamhost.com/index.cgi?tree=goodies.mysql"
print

def testDB(db_hostname, db_username, db_password, db_database):
    def _sigALRM(sig, frame): pass
    signal.signal(signal.SIGALRM, _sigALRM)
    signal.alarm(5)
    db = MySQLdb.connect(db_hostname, db_username, db_password, db_database)
    signal.alarm(0)

while True:
    db_hostname = raw_input("MySQL hostname: ").strip()
    db_database = raw_input(" Database name: ").strip()
    db_username = raw_input("MySQL username: ").strip()
    db_password = raw_input("  and password: ").strip()
    print "Checking connection... ",
    try:
        testDB(db_hostname, db_username, db_password, db_database)
        print "looks good!"
        break
    except Exception, e:
        print "oops, that didn't work:", e
        print

print "Creating project framework... ",
if os.spawnl(os.P_WAIT, "/usr/bin/django-admin.py", "django-admin.py", "startproject", projname) != 0:
    print "oops, django-admin failed to run!"
    sys.exit(1)

print "creating passenger_wsgi.py... ",
f = open("passenger_wsgi.py", "w")
f.write("""import sys, os
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = "%s.settings"
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
""" % projname)
f.close()

print "customizing settings... ",

settings = open("%s/settings.py" % projname, "r").read()
urls = open("%s/urls.py" % projname, "r").read()

# Fill in blanks
for key, value in {
        'DATABASE_ENGINE': "mysql",
        'DATABASE_HOST': db_hostname,
        'DATABASE_NAME': db_database,
        'DATABASE_USER': db_username,
        'DATABASE_PASSWORD': db_password,
        'MEDIA_ROOT': os.path.join(os.getcwd(), 'public/media'),
        'MEDIA_URL': '/media/',
    }.items(): settings = re.sub(r'(?<=\n)%s\s*=.*(?=[\n#])' % key, r'%s = %r' % (key, value), settings)

# newer Django db settings use this:
for key, value in {
        'ENGINE': "django.db.backends.mysql",
        'HOST': db_hostname,
        'NAME': db_database,
        'USER': db_username,
        'PASSWORD': db_password,
        }.items(): settings = re.sub(r"'%s':\s*'.*?'," % key, "%r: %r," % (key, value), settings)

# Enable admin stuff
settings = settings.replace("INSTALLED_APPS = (\n", "INSTALLED_APPS = (\n    'django.contrib.admin',\n")
urls = urls.replace("# from", "from")
urls = urls.replace("# admin", "admin")
urls = urls.replace("# (r'^admin", "(r'^admin")

open("%s/settings.py" % projname, "w").write(settings)
open("%s/urls.py" % projname, "w").write(urls)

# Permissions
print "setting permissions... ",
os.chmod(projname, 0750)
os.chmod(os.path.join(projname, "manage.py"), 0755)

# copy admin media
print "copying admin media... ",
if os.spawnl(os.P_WAIT, "/bin/cp", "cp", "-rL", os.path.join(imp.find_module("django")[1], "contrib/admin/media"), "public") != 0:
    print "oops, file copy failed!"
    sys.exit(1)

print "OK"

# syncdb!
print "Running manage.py syncdb..."
if os.spawnl(os.P_WAIT, "./%s/manage.py" % projname, "manage.py", "syncdb") != 0:
    print "oops, manage.py failed!"
    sys.exit(1)

# createsuperuser
print "Creating a Django superuser..."
if os.spawnl(os.P_WAIT, "./%s/manage.py" % projname, "manage.py", "createsuperuser") != 0:
    print "Or not."

print
print
print "\a\033[1;32mSUCCESS!\033[m Your Django application is fully set up - enjoy!"
print