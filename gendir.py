from pathlib import Path
import yaml

def gen_dir(working_dir, username, suffix):
    if isinstance(working_dir, str):
        working_dir = Path(working_dir)
    return working_dir / '{}{}'.format(username, suffix)

def repo(config, username):
    with open(config, 'r') as file:
        cfg = yaml.load(file)
    repo_dir = cfg['users'][username].get('repo_local', None)
    if repo_dir is None:
        repo_dir = '{}_repo'.format(username)
    return Path(cfg['working_dir']) / repo_dir

def venv(working_dir, username):
    return gen_dir(working_dir, username, '_venv')

def result(working_dir, username):
    return gen_dir(working_dir, username, '_results')