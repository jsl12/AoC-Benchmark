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


def run_profiler(venv_dir, user_src_dir, inputs_dir):
    py = venv_dir / 'Scripts' / 'python.exe'
    cmd = [str(py), 'prof.py', '-rp', str(user_src_dir), '-ip', str(inputs_dir)]
    subprocess.run(cmd)

@click.command()
@click.option('--users', help='users.yaml file')
def from_user_config(users):
    cfg = yaml.load(open(users, 'r'))
    working_dir = Path(cfg['working_dir'])

    logging.info('Fetching Inputs')
    inputs_dir = working_dir / INPUTS_DIR
    gitsync.sync_repo(cfg['input']['repo_url'], str(inputs_dir))

    for u in cfg['users']:
        username = list(u)[0]
        user = u[username]
        logging.info('Building environment for {}'.format(username))
        git_path = gendir.repo(working_dir, username)
        venv_path = gendir.venv(working_dir, username)
        build_env(user['repo_url'], git_path, venv_path)

        logging.info('Computing benchmarks for {}'.format(username))
        run_profiler(venv_path, git_path, inputs_dir)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from_user_config()