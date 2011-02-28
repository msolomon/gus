# Django settings for gus project.
import os
from django.core.urlresolvers import get_script_prefix
PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'guspy.db', # Or path to database file if using sqlite3.
        'USER': 'guspy', # Not used with sqlite3.
        'PASSWORD': 'chandler is a little girl', # Not used with sqlite3.
        'HOST': 'johnls.net', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'
#BASE_URL = get_script_prefix()
#print BASE_URL
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, '../views')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#  MEDIA_URL = "include/" - this is set in root urls.py to allow dynamic urls

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = 'media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^nat@lnqd0wmfr9gyw8&o_l(v2=uwr+524(1g!a!@!thf17m&k'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'gus.urls'



TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, '../views'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'gus.gus_gallery',
    'gus.gus_groups',
    'gus.gus_roles',
    'gus.gus_users',
    'gus.gus_calendar',
    'gus.gus_widget',
    'gus.gus_forum',
    'gus.gus_emailer',
    'gus.gus_bill',
    'gus.gusTestSuite'

    
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

#The first line of code sets a custom test runner, instead of the default one django uses. We need the custom one
# in order to include the coverage library that will run our coverage tests.
#The 'coverage.py' library can be obtained from the following site:
#            http://pypi.python.org/pypi/coverage

#The second line of code tells the coverage library what to cover. I've got all of our current modules here, 
#but if we ever have more, we'll have to insert them


TEST_RUNNER='gus.tests.test_runner_with_coverage'
modules = 'bill calendar emailer forum gallery groups users roles widget'
COVERAGE_MODULES = []
for m in modules.split():
	COVERAGE_MODULES.append('gus.gus_%s.models' % m)
	COVERAGE_MODULES.append('gus.gus_%s.views' % m)

## Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'guspyuser@gmail.com'
EMAIL_HOST_PASSWORD = 'givemegus'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = '[gus] '
