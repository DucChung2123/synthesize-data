import abc 

class ConfigReaderInterface(abc.ABC):
    
    def __init__(self):
        super().__init__()
        
    def read_config(self, config_file: str):
        raise NotImplementedError