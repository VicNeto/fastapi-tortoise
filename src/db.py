from pathlib import Path
from dotenv import load_dotenv
import os
dir_path = Path(os.path.dirname(os.path.abspath(__file__)))
PARENT_DIR = dir_path.parent
load_dotenv(os.path.join(PARENT_DIR, ".env"))

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