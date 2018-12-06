import gitsync
import venvbuild
import os
from pathlib import Path
import yaml
import click
import logging
import subprocess

import gendir

INPUTS_DIR = 'AoC-Inputs'

def build_env(giturl, git_dir, venv_dir):
    gitsync.sync_repo(giturl, git_dir)
    venvbuild.create_venv(venv_dir)

    user_reqs = os.path.join(git_dir, 'requirements.txt')
    venvbuild.pip_install_requirements(venv_dir, user_reqs)

    profiler_reqs = 'profiler_requirements.txt'
    venvbuild.pip_install_requirements(venv_dir, profiler_reqs)


def run_profiler(username, config_path):
    with open(config_path, 'r') as file:
        cfg = yaml.load(file)
    working_dir = Path(cfg['working_dir'])
    py_path = gendir.venv(working_dir, username) / 'Scripts' / 'python.exe'
    cmd = [str(py_path), 'prof.py']
    cmds = [
        ('rp', gendir.repo(config_path, username)),
        ('ip', working_dir / INPUTS_DIR),
        ('u', username)
    ]
    for c in cmds:
        cmd.extend(['-{}'.format(c[0]), str(c[1])])
    subprocess.run(cmd)

@click.command()
@click.option('--users', help='users.yaml file')
def from_user_config(users):
    cfg = yaml.load(open(users, 'r'))
    working_dir = Path(cfg['working_dir'])

    logging.info('Fetching Inputs')
    inputs_dir = working_dir / INPUTS_DIR
    gitsync.sync_repo(cfg['input']['repo_url'], str(inputs_dir))

    for username in cfg['users']:
        logging.info('Building environment for {}'.format(username))
        git_path = gendir.repo(users, username)
        venv_path = gendir.venv(working_dir, username)
        build_env(cfg[username]['repo_url'], git_path, venv_path)

        logging.info('Computing benchmarks for {}'.format(username))
        run_profiler(username, users)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from_user_config()