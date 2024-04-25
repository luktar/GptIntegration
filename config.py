from dataclasses import dataclass
import json

@dataclass
class Config:
    openai_apikey: str


def load_config(config_file):
    with open(config_file, 'r') as file:
        config_data = json.load(file)
    return Config(**config_data)