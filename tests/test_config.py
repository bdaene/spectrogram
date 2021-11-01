from copy import deepcopy

from spectrogram.config import config, load_config
from tests.conftest import SAMPLES_PATH


def test_load_config():
    expected_config = deepcopy(config)
    expected_config.update({
        'parameter_a': 'a',
        'parameter_b': {
            'parameter_b1': 1,
            'parameter_b2': [5, 2],
        }
    })

    load_config(SAMPLES_PATH / 'config.yml')

    assert config == expected_config
