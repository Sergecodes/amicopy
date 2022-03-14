import os
from decouple import config, Csv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'users.User'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
SECRET_KEY = config('SECRET_KEY')
USE_CONSOLE_EMAIL = config('USE_CONSOLE_EMAIL', default=True, cast=bool)

# DB
USE_PROD_DB = config('USE_PROD_DB', cast=bool)
DB_USER = config('DB_USER')
DB_NAME = config('DB_NAME')
DB_PASSWORD = config('DB_PASSWORD')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')

# AWS
USE_S3 = config('USE_S3', default=False, cast=bool)
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')

# REDIS
USE_REDIS = config('USE_REDIS', default=True, cast=bool)
REDIS_PORT = config('REDIS_PORT', cast=int)


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if USE_PROD_DB:
	pass
else:
	DATABASES = {
		# Configure database with schemas
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'OPTIONS': {
				# Use `django` schema so as not to polute public schema
				'options': '-c search_path=django,public'
			},
			'NAME': DB_NAME,
			'USER': DB_USER,
			'PASSWORD': DB_PASSWORD,
			'HOST': DB_HOST,
			'PORT': DB_PORT,
		},
		'users': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'OPTIONS': {
				'options': '-c search_path=users,public'
			},
			'NAME': DB_NAME,
			'USER': DB_USER,
			'PASSWORD': DB_PASSWORD,
			'HOST': DB_HOST,
			'PORT': DB_PORT,
		},
		'transactions': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'OPTIONS': {
				'options': '-c search_path=transactions,public'
			},
			'NAME': DB_NAME,
			'USER': DB_USER,
			'PASSWORD': DB_PASSWORD,
			'HOST': DB_HOST,
			'PORT': DB_PORT,
		},
		'notifications': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'OPTIONS': {
				'options': '-c search_path=notifications,public'
			},
			'NAME': DB_NAME,
			'USER': DB_USER,
			'PASSWORD': DB_PASSWORD,
			'HOST': DB_HOST,
			'PORT': DB_PORT,
		},
		'subscriptions': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'OPTIONS': {
				'options': '-c search_path=subscriptions,public'
			},
			'NAME': DB_NAME,
			'USER': DB_USER,
			'PASSWORD': DB_PASSWORD,
			'HOST': DB_HOST,
			'PORT': DB_PORT,
		}
	}


if USE_CONSOLE_EMAIL:
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
	# TODO  set up email
	# EMAIL_HOST = config('EMAIL_HOST', default='localhost')
	# EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
	# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
	# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
	# EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
	pass


# Application definition

INSTALLED_APPS = [
	# django-grappelli should be placed before django.contrib.admin
	'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

	# Project apps
	'core',
	'notifications',
	'subscriptions',
	'transactions',
	'users',

    # Third-party apps
	'channels',
	'ckeditor',
	'django_extensions',
	
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'amicopy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'amicopy.wsgi.application'

# Added
ASGI_APPLICATION = "amicopy.asgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Caching TODO use redis instead in production!! (even before production!)
# CACHES = {
# 	'default': {
# 		'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
# 		'TIMEOUT': 300,  # The default(300s = 5mins)
# 		# 'TIMEOUT': 60 * 60 * 24,  # 86400(s)=24h
# 	}
# }


# Use this to configure the test databases and schema during first run.
# TEST_RUNNER = 'core.tests.runner.PostgresSchemaTestRunner'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
if USE_S3:
	AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
	AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
	AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
	AWS_S3_SIGNATURE_VERSION = 's3v4'
	AWS_S3_REGION_NAME = 'us-east-1'
	AWS_S3_FILE_OVERWRITE = False
	AWS_DEFAULT_ACL = None
	AWS_S3_VERIFY = True

	## Note: Variables ending in '_' are user-defined, not required or used by a package
	AWS_S3_CUSTOM_DOMAIN_ = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
	AWS_S3_OBJECT_PARAMETERS = {
		# use a high value so that files are cached for long (6months=2628000)
		# however, updates on files won't work ... and file name  should be changed after updates..
		# for now, set it to 1 day(86400secs)
		# 1month = 2.628e+6 (2628000secs)
		'CacheControl': 'max-age=86400'
	}
	# s3 static settings
	STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN_}/static/'
	STATICFILES_STORAGE = 'core.storages.StaticStorage'
	# STATIC_ROOT isn't needed here

	# s3 public media settings. 
	# This var is also used in core.storages to set the location of media files
	MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN_}/media/'
	# MEDIA_ROOT isn't also needed here
	# MEDIA_ROOT = MEDIA_URL
	DEFAULT_FILE_STORAGE = 'core.storages.PublicMediaStorage'

	# # s3 private media settings
	# PRIVATE_MEDIA_LOCATION = 'private'
	# PRIVATE_FILE_STORAGE = 'core.storages.PrivateMediaStorage'
else:
	DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'  
	STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
	STATIC_URL = '/static/'
	STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
	# STATICFILES_DIRS = [
	# 	BASE_DIR / 'static'
	# ]

	MEDIA_URL = 'media/'
	MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


## THIRD-PARTY APPS CONFIG
## channels
if USE_REDIS:
	CHANNEL_LAYERS = {
		"default": {
			"BACKEND": "channels_redis.core.RedisChannelLayer",
			"CONFIG": {
				"hosts": [("localhost", REDIS_PORT)],
			},
		},
	}
else:
	CHANNEL_LAYERS = {
		"default": {
			"BACKEND": "channels.layers.InMemoryChannelLayer"
		}
	}


## ckeditor
# Plugins: though not all are enabled by default
# a11yhelp, about, adobeair, ajax, autoembed, autogrow, autolink, bbcode, clipboard, codesnippet,
# codesnippetgeshi, colordialog, devtools, dialog, div, divarea, docprops, embed, embedbase,
# embedsemantic, filetools, find, flash, forms, iframe, iframedialog, image, image2, language,
# lineutils, link, liststyle, magicline, mathjax, menubutton, notification, notificationaggregator,
# pagebreak, pastefromword, placeholder, preview, scayt, sharedspace, showblocks, smiley,
# sourcedialog, specialchar, stylesheetparser, table, tableresize, tabletools, templates, uicolor,
# uploadimage, uploadwidget, widget, wsc, xml

# uploadimage plugin is responsible for image/file upload
CKEDITOR_CONFIGS = {
	'default': {
		'skin': 'moono',
        # 'skin': 'office2013',
		'toolbar': 'full',
		'removePlugins': '',
		'width': 'auto',
		# 'extraPlugins': 'codesnippet,clipboard', 
	},
	'test': {
		'skin': 'moono',
        # 'skin': 'office2013',
		'toolbar': 'Custom',
		'toolbar_Custom': [
			['Bold', 'Italic', ],
			# codesnippet plugin needs to be loaded for CodeSnippet to work.
			['Link', 'Blockquote', 'Clipboard', 'CodeSnippet'],
			['NumberedList', 'BulletedList', 'Format', 'HorizontalRule'],
			['Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight'],
			['Undo', 'Redo'],
			['Maximize', 'Preview']
		],
		'tabSpaces': 4,
		'width': 'auto',
		# 'uiColor': '#ff3333',
	},
}

