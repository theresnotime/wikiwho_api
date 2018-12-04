from .settings_base import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
SERVER_LEVEL = LEVEL_STAGING
ACTIONS_LOGS = '/home/ww_staging/actions_logs'
ACTIONS_MAX_WORKERS = 4

ACTIONS_LANGUAGES = ['tr', 'eu', 'es', 'de', 'en']
CRONJOBS = [
    ('* 23 7 * *', 'api_editor.cron.update_actions_tables', f'>> /dev/null 2>> /var/log/django/crontab.log')
]


INSTALLED_APPS += ['debug_toolbar',
                   'debug_panel']

MIDDLEWARE_CLASSES += ['debug_panel.middleware.DebugPanelMiddleware']

SWAGGER_SETTINGS['VALIDATOR_URL'] = 'https://online.swagger.io/validator'

ONLY_READ_ALLOWED = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
