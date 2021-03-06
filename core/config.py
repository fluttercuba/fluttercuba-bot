import yaml
from dataclasses import dataclass


@dataclass
class SettingFile():
    file_path: str

    def load_external_services_file(self) -> dict:
        with open(self.file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
