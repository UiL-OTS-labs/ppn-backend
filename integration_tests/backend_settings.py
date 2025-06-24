import sys
sys.path.append('../backend')

from ppn_backend.settings import *

FIXTURE_DIRS = ['data_fixtures']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'backend.int.db.sqlite3',
    }}