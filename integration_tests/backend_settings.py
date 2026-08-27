import sys
sys.path.append('../backend')

from ppn_backend.settings import *

DATABASES['default']['NAME'] = 'ppn_test'
FIXTURE_DIRS = ['data_fixtures']
DATABASES['default']['NAME'] = 'ppn-test'
