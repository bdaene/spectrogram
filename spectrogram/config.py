
import importlib.resources

import yaml

config = {}


def load_config(config_path=None):

    if config_path is None:
        config_stream = importlib.resources.open_text("spectrogram", "default_config.yml")
    else:
        config_stream = open(config_path)

    with config_stream:
        config.update(yaml.load(config_stream, Loader=yaml.FullLoader))
