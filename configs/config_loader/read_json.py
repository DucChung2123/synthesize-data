import json
from abc import ABC
from pathlib import Path

from configs.config_loader.config_interface import ConfigReaderInterface

class JsonConfigReader(ConfigReaderInterface):

    def __init__(self):
        super(JsonConfigReader, self).__init__()

    def read_config(self, config_file: str):
        with open(config_file) as file:
            config = json.load(file)
        return config