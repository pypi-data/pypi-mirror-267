import os
import yaml

# default_config.py
_global_config = {
    'key1': 'value1',
    'wrap': False,
    'adjust_to_ratio': True,
    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    'ratio': (5**.5 - 1) / 2,
}

if os.path.isfile('./.latex_export.yaml'):
    with open('./.latex_export.yaml') as f:
        _global_config.update(yaml.safe_load(f))


def update_config(config_change):
    _global_config.update(config_change)

def get_config(arg, raise_exception=True):
    if arg in _global_config:
        return _global_config[arg]
    else:
        if raise_exception:
            raise Exception("Config not set: " + arg)
        else:
            return None

class TikzConfig:
    def __init__(self, config_change):
        self.config_change = config_change

    def __enter__(self):
        global _global_config
        self.old_config = _global_config
        _global_config = _global_config | self.config_change
        return _global_config

    def __exit__(self, exc_type, exc_value, traceback):
        global _global_config
        _global_config = self.old_config