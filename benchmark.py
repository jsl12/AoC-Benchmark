import gitsync
import venvbuild
import os
import click
import logging
import subprocess

import cfg

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


def run_profiler(username, config):
    c = config
    py_path = c.venv(username) / 'Scripts' / 'python.exe'
    cmd = [str(py_path), 'prof.py']
    cmds = [
        ('rp', c.repo(username)),
        ('ip', c.inputs_dir),
        ('u', username),
        ('to', c.timeout),
        ('uc', c.path)
    ]
    for c in cmds:
        cmd.extend(['-{}'.format(c[0]), str(c[1])])
    subprocess.run(cmd)

@click.command()
@click.option('--config_path', help='users.yaml file')
def from_user_config(config_path):
    logging.info('Configuring benchmark platform with {}'.format(config_path))
    c = cfg.Config(config_path)

    logging.info('Fetching Inputs')
    gitsync.sync_repo(
        repo_url=c.inputs_url,
        dest_dir=str(c.inputs_dir)
    )

    for username in c.users:
        build_env(c.repo_url(username), c.repo(username), c.venv(username))

        logging.info('Running benchmarks for {}'.format(username))
        run_profiler(username, c)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from_user_config()