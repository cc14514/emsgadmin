#/usr/bin/env python
#coding=utf8
import os.path as op
# Django settings for emsgadmin project.

# True 测试环境，False 生产环境
DEBUG = True

if DEBUG:
####################################################
# 测试环境
####################################################
    #emsg_inf_push_host = '192.168.12.212'
    #emsg_inf_push_port = 4281 
    #emsg_service_url = "http://192.168.12.212:4280/"
    fileserver_service_url = "http://192.168.12.213:8000/"
    mongo_host = '192.168.12.213'
    mongo_port = 27017
    mongo_replicaset = 'part1'

    ALLOWED_HOSTS = []
    STATIC_ROOT = '/app/static'
else:
####################################################
# 生产环境 
####################################################
    #emsg_inf_push_host = '192.168.2.101'
    #emsg_inf_push_port = 4281 
    #emsg_service_url = 'http://192.168.2.101:4280/'
    #这个服务只在内网开放，所以用的是 uwsgi 内网的 http 地址
    fileserver_service_url = "http://192.168.0.7:9091/"
    mongo_host = '192.168.0.6'
    mongo_port = 27017
    mongo_replicaset = 'lc'
    ALLOWED_HOSTS = [ 'localhost', '127.0.0.1', '192.168.0.6', "fileserver.qiuyouzone.com",]
    STATIC_ROOT = '/home/appusr/www/static'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': op.join(op.dirname(__file__),'data','emsgadmin.db'),                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

TEMPLATE_DEBUG = DEBUG
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Chongqing'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

import os.path as op
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	op.join(op.dirname(__file__),'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j7la!x1a#o**j4921_ivcavz6#i$j8!cd@=^4lub4#6j%y55^='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'emsgadmin.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'emsgadmin.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	op.join(op.dirname(__file__),'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'emsgadmin.admin',
	'domain',
	'mgr',
    'myTags',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = { 
	'version': 1, 
	'disable_existing_loggers': False, 
	'filters': { 
		'require_debug_false': { 
			'()': 'django.utils.log.RequireDebugFalse' 
		} 
	}, 
	'formatters': { 
		'verbose': { 
			'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s' 
		}, 
		'simple': { 
			'format': '%(levelname)s %(message)s' 
		}, 
	}, 
	'handlers': { 
		'mail_admins': { 
			'level': 'ERROR', 
			'filters': ['require_debug_false'], 
			'class': 'django.utils.log.AdminEmailHandler' 
		}, 
		'console':{ 
			'level':'DEBUG', 
			'class':'logging.StreamHandler', 
			'formatter':'simple' 
		}, 
		'file':{ 
			'level':'DEBUG', 
			'class':'logging.FileHandler', 
			'filename':'/tmp/emsgadmin.log', 
			'formatter':'verbose', 
		} 
	}, 
	'loggers': { 
		'django.request': { 
			'handlers': ['file'], 
			'level': 'ERROR', 
			'propagate': True, 
		}, 
		'emsgadmin':{ 
            'handlers': ['file','console'], 
            'level': 'DEBUG', 
            'propagate': True, 
        },
        'mgr':{ 
            'handlers': ['file','console'], 
            'level': 'DEBUG', 
            'propagate': True, 
        } 
	} 
}

# 拦截器配置
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)