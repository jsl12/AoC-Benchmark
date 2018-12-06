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


def run_profiler(config_path, username):
    cfg = gendir.readconfig(config_path)
    working_dir = Path(cfg['working_dir'])
    py_path = gendir.venv(config_path, username) / 'Scripts' / 'python.exe'
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
@click.option('--config_path', help='users.yaml file')
def from_user_config(config_path):
    cfg = gendir.readconfig(config_path)
    working_dir = Path(cfg['working_dir'])

    logging.info('Fetching Inputs')
    inputs_dir = working_dir / INPUTS_DIR
    gitsync.sync_repo(cfg['input']['repo_url'], str(inputs_dir))

    for username in cfg['users']:
        logging.info('Building environment for {}'.format(username))
        git_path = gendir.repo(config_path, username)
        venv_path = gendir.venv(config_path, username)
        build_env(str(gendir.repo(config_path, username)), git_path, venv_path)

        logging.info('Computing benchmarks for {}'.format(username))
        run_profiler(config_path, username)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from_user_config()