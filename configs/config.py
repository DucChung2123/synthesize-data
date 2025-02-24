import logging
from configs.config_loader import ConfigReaderInstance

class Config:
    """Returns a config instance depending on the ENV_STATE variable."""
    def __init__(self, args=None):
        settings_params = getattr(args, 'override_default_config', "settings/config.yml")
        try:
            self.CONF = ConfigReaderInstance.yaml.read_config_from_file(settings_params)
        except Exception as e:
            logging.error(f"Failed to read config file {settings_params}: {e}")
            raise

def set_config(args=None):
    global settings
    settings = Config(args)