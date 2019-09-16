import json
import os
from pathlib import Path


testing = os.environ.get('GXENV_TEST', None) is not None
env_base = None

if testing:
    env_base = "/tmp/"


def load_config(path):
    global env_base

    if testing:
        return

    with open(path, 'r') as f:
        config = json.load(f)
    env_base = config["env_base"]


global_config = Path('/') / 'etc' / 'gxenv' / 'config.json'
home_config = Path.home() / '.config' / 'gxenv' / 'config.json'

if global_config.exists():
    load_config(home_config)

if home_config.exists():
    load_config(home_config)

if env_base is None:
    print('WARNING: env base path is not configured. Falling back to /tmp. To change it, please create a config in ~/.config/gxenv/config.json or /etc/gxenv/config.json.')
    env_base = '/tmp/'

env_path_tmpl = env_base + "{}"
test_env_name = "testenv"

