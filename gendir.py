from pathlib import Path
import yaml
import functools

@functools.lru_cache(maxsize=1)
def readconfig(config_path):
    with open(config_path, 'r') as file:
        return yaml.load(file)

def repo(config_path, username):
    cfg = readconfig(config_path)
    repo_dir = cfg['users'][username].get('repo_local', None)
    if repo_dir is None:
        repo_dir = '{}_repo'.format(username)
    return Path(cfg['working_dir']) / repo_dir

def venv(config_path, username):
    cfg = readconfig(config_path)
    venv_dir = cfg['users'][username].get('venv_local', None)
    if venv_dir is None:
        venv_dir = '{}_repo'.format(username)
    return Path(cfg['working_dir']) / venv_dir

def results(config_path, username):
    cfg = readconfig(config_path)
    result_dir = cfg['users'][username].get('results', None)
    if result_dir is None:
        result_dir = '{}_results'.format(username)
    return Path(cfg['working_dir']) / result_dir