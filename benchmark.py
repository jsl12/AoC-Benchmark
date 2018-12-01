import gitsync
import venvbuild
import os
import configparser
import click
import logging
import subprocess

INPUTS_DIR = 'AoC-Inputs'

def build_env(giturl, git_dir, venv_dir):
    gitsync.sync_repo(giturl, git_dir)
    venvbuild.create_venv(venv_dir)

    user_reqs = os.path.join(git_dir, 'requirements.txt')
    venvbuild.pip_install_requirements(venv_dir, user_reqs)

    profiler_reqs = 'profiler_requirements.txt'
    venvbuild.pip_install_requirements(venv_dir, profiler_reqs)


def run_profiler(venv_dir, user_src_dir, inputs_dir):
    cmd = [os.path.join(venv_dir, 'Scripts', 'python.exe'), 'prof.py', '-rp', user_src_dir, '-ip', inputs_dir]
    subprocess.run(cmd)

@click.command()
@click.option('--users', help='users.ini file')
def from_users_ini(users):
    cfg = configparser.ConfigParser() #TODO refactor out configparser into a seperate func
    cfg.read(users)
    usernames = [s for s in cfg.sections() if s != 'Config']

    logging.info('Fetching Inputs')
    gitsync.sync_repo(cfg['Config']['INPUT_REPO_URL'].strip(), INPUTS_DIR)

    for user in usernames:
        logging.info('Building environment for {}')
        git_url = cfg[user]['REPO_URL'].strip()
        git_path = user + '_repo'
        venv_path = user + '_venv'
        build_env(git_url, git_path, venv_path)

        logging.info('Computing benchmarks for {}'.format(user))

        run_profiler(venv_path, git_path, INPUTS_DIR)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from_users_ini()