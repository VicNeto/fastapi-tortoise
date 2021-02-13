import os

TORTOISE_ORM = {
    'connections': {
        'default': os.getenv("DB_URL")
    },
    'apps': {
        'models': {
            'models': ['models', 'aerich.models'],
            'default_connection': 'default',
        }
    }
}