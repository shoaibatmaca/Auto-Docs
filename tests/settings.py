SECRET_KEY = 'test-secret-key-for-testing-only'
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework',
    'autoapi_swagger',
]

MIDDLEWARE = []

ROOT_URLCONF = 'tests.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

USE_TZ = True

REST_FRAMEWORK = {}

