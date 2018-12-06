from pathlib import Path
import yaml
import functools

@functools.lru_cache(maxsize=1)
def readconfig(config_path):
    with open(config_path, 'r') as file:
        return yaml.load(file)

def gen_dir(working_dir, username, suffix):
    if isinstance(working_dir, str):
        working_dir = Path(working_dir)
    return working_dir / '{}{}'.format(username, suffix)

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

def result(working_dir, username):
    return gen_dir(working_dir, username, '_results')