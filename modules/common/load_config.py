import os
import json
from typing import Dict, Any

from dotenv import load_dotenv

load_dotenv()


class Configuration:
    @staticmethod
    def get_config() -> Dict[str, Any]:
        config_path = os.path.join(os.getcwd(), 'configuration\\config.json')
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
            return config
