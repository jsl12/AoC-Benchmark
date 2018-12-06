from pathlib import Path

def gen_dir(working_dir, username, suffix):
    if isinstance(working_dir, str):
        working_dir = Path(working_dir)
    return working_dir / '{}{}'.format(username, suffix)

def repo(working_dir, username):
    return gen_dir(working_dir, username, '_repo')

def venv(working_dir, username):
    return gen_dir(working_dir, username, '_venv')

def result(working_dir, username):
    return gen_dir(working_dir, username, '_results')