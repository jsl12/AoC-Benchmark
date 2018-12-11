import click
import compare
import gitsync
import logging
import os
import subprocess
import venvbuild

import config

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


def run_profiler(username, config_file):
    py_path = config_file.venv(username) / 'Scripts' / 'python.exe'
    cmd = [str(py_path), 'prof.py']
    cmds = [
        ('rp', config_file.repo(username)),
        ('ip', config_file.inputs_dir),
        ('resp', config_file.results(username)),
        ('to', config_file.timeout),
        ('n', config_file.n)
    ]
    for c in cmds:
        cmd.extend(['-{}'.format(c[0]), str(c[1])])
    logging.debug(cmd)
    subprocess.run(cmd)

@click.command()
@click.option('--config_path', help='users.yaml file')
def from_user_config(config_path):
    logging.info('Configuring benchmark platform with {}'.format(config_path))
    cfg = config.Config(config_path)

    logging.info('Fetching Inputs')
    gitsync.sync_repo(
        repo_url=cfg.inputs_url,
        dest_dir=str(cfg.inputs_dir)
    )

    for username in cfg.users:
        build_env(cfg.repo_url(username), cfg.repo(username), cfg.venv(username))

        logging.info('Running benchmarks for {}'.format(username))
        run_profiler(username, cfg)

    compare.plot_comparison(config_path, '2018 comparison.png')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from_user_config()