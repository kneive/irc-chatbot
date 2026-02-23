import json
import os
from pathlib import Path

CONFIG = Path(__file__).parent.parent / 'config' / 'cors_config.json'

def load_config(env=None):
    """Load CORS configuration from ../config/cors_config.json"""

    if env is None:
        env = os.getenv('FLASK_ENV', 'development')

    if not CONFIG.exists():
        print(f"WARNING: configuration file {CONFIG} not found. Using default.")
        return {
            'origins': ['0.0.0.0:5000'],
            'methods': ['GET'],
            'allow_credentials': False,
            'max_age': 3600
        }

    with open(CONFIG) as conf:
        all_configurations = json.load(conf)

    config = all_configurations.get(env, all_configurations.get('development'))

    return config