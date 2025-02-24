from pathlib import Path

import yaml

from configs.config_loader.config_interface import ConfigReaderInterface

class YamlConfigReader(ConfigReaderInterface):

    def __init__(self):
        super(YamlConfigReader, self).__init__()

    def read_config_from_file(self, config_file: str):
        with open(config_file) as file:
            config = yaml.safe_load(file)
        return config