# import raven

from .settings_base import *

# TODO https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
SERVER_LEVEL = LEVEL_PRODUCTION

ACTIONS_LOG = '/var/log/django/actions_log'
ACTIONS_MAX_WORKERS = 12
EVENTS_STREAM_LOG = '/var/log/django/events_streamer'

SWAGGER_SETTINGS['VALIDATOR_URL'] = 'https://online.swagger.io/validator'

ALLOWED_HOSTS = ['wikiwho-api.wmcloud.org', 'wikiwho.wmflabs.org']

ONLY_READ_ALLOWED = False

ACTIONS_LANGUAGES = ['ar', 'de', 'en', 'es', 'eu', 'fr', 'hu', 'id', 'it', 'ja', 'nl', 'pl', 'pt', 'tr']
EVENT_STREAM_WIKIS = ['arwiki', 'dewiki', 'enwiki', 'eswiki', 'euwiki', 'frwiki', 'huwiki', 'idwiki', 'itwiki', 'jawiki', 'nlwiki', 'plwiki', 'ptwiki', 'trwiki']

# On pickle_storage volume, mounted to /pickles
PICKLE_FOLDER_DE = '/pickles/de'
PICKLE_FOLDER_EN = '/pickles/en'
PICKLE_FOLDER_ES = '/pickles/es'
PICKLE_FOLDER_EU = '/pickles/eu'
PICKLE_FOLDER_TR = '/pickles/tr'

# On pickle_storage02 volume, mounted to /pickles-02
PICKLE_FOLDER_AR = '/pickles-02/ar'
PICKLE_FOLDER_FR = '/pickles-02/fr'
PICKLE_FOLDER_HU = '/pickles-02/hu'
PICKLE_FOLDER_ID = '/pickles-02/id'
PICKLE_FOLDER_IT = '/pickles-02/it'
PICKLE_FOLDER_JA = '/pickles-02/ja'
PICKLE_FOLDER_NL = '/pickles-02/nl'
PICKLE_FOLDER_PL = '/pickles-02/pl'
PICKLE_FOLDER_PT = '/pickles-02/pt'

REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['anon'] = '100/sec'
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['burst'] = '100/sec'
