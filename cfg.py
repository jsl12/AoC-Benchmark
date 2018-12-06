from pathlib import Path
import yaml
import functools

# Option to monkey-patch once and avoid having to pass around the config_path argument
CONFIG_PATH = None

@functools.lru_cache(maxsize=1)
def readconfig(config_path=None):
    # The idea here is that you can monkey-patch CONFIG_PATH to initialize and then
    # avoid having to pass around the path to the config file for subsequent calls.
    # Setting the cache size to 1 means that every time this function sees a new input
    # it caches the result.
    # Usage:
    #   - readconfig is called with a real path, e.g. users.yaml
    #   - CONFIG_PATH gets set to the real path
    #   - readconfig is called again, but without an argument
    #   - the value of CONFIG_PATH gets used
    #   - functools caches the result as having come from the input None
    #   - readconfig is called subsequent times without an argument
    #   - functools returns the cached result
    global CONFIG_PATH

    if config_path is not None:
        CONFIG_PATH = config_path
    elif config_path is None and CONFIG_PATH is not None:
        config_path = CONFIG_PATH
    else:
        assert config_path is not None, 'cfg.CONFIG_PATH was not initialized'

    with open(config_path, 'r') as file:
        return yaml.load(file)

def working_dir(config_path):
    return Path(readconfig(config_path)['working_dir'])

def inputs_dir(config_path=None):
    return working_dir(config_path) / readconfig(config_path)['input']['repo_local']

def inputs_repo(config_path=None):
    return readconfig(config_path)['input']['repo_url']

def repo_url(username, config_path=None):
    return readconfig(config_path)['users'][username]['repo_url']

def user_dir(username, name, suffix, config_path=None):
    dir = readconfig(config_path)['users'][username].get(name, None)
    if dir is None:
        dir = '{}_{}'.format(username, suffix)
    res = working_dir(config_path) / dir
    if not res.exists():
        res.mkdir()
    return res

def repo(username, config_path=None):
    return user_dir(username, 'repo_local', '_repo', config_path)

def venv(username, config_path=None):
    return user_dir(username, 'venv_local', '_venv', config_path)

def results(username, config_path=None):
    return user_dir(username, 'results', '_results', config_path) / readconfig(config_path)['res_filename']

