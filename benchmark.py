import gitsync
import venvbuild
import os
import click
import logging
import subprocess

import gendir

INPUTS_DIR = 'AoC-Inputs'

def build_env(giturl, git_dir, venv_dir):
    logging.info('Syncing solution repo')
    gitsync.sync_repo(giturl, git_dir)

    logging.info('Building user venv')
    venvbuild.create_venv(venv_dir)

    logging.info('Installing solution requirements')
    user_reqs = os.path.join(git_dir, 'requirements.txt')
    venvbuild.pip_install_requirements(venv_dir, user_reqs)

    logging.info('Installing profiler requirements')
    profiler_reqs = 'profiler_requirements.txt'
    venvbuild.pip_install_requirements(venv_dir, profiler_reqs)


def run_profiler(config_path, username):
    py_path = gendir.venv(config_path, username) / 'Scripts' / 'python.exe'
    cmd = [str(py_path), 'prof.py']
    cmds = [
        ('rp', gendir.repo(config_path, username)),
        ('ip', gendir.inputs_dir(config_path)),
        ('u', username),
        ('to', gendir.readconfig(config_path)['timeout'])
    ]
    for c in cmds:
        cmd.extend(['-{}'.format(c[0]), str(c[1])])
    subprocess.run(cmd)

@click.command()
@click.option('--config_path', help='users.yaml file')
def from_user_config(config_path):
    logging.info('Fetching Inputs')
    gitsync.sync_repo(
        repo_url=gendir.inputs_repo(config_path),
        dest_dir=str(gendir.inputs_dir(config_path))
    )

    cfg = gendir.readconfig(config_path)
    for username in cfg['users']:
        git_url = gendir.repo_url(config_path, username)
        git_path = gendir.repo(config_path, username)
        venv_path = gendir.venv(config_path, username)
        build_env(git_url, git_path, venv_path)

        logging.info('Running benchmarks for {}'.format(username))
        run_profiler(config_path, username)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from_user_config()