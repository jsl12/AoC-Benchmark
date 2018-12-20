from pathlib import Path
import click
import compare
import config
import gitsync
import logging
import os
import subprocess
import venvbuild

def setup_input_repo(config):
    logging.info('Setting up input repo from {}'.format(config.inputs_url))
    gitsync.sync_repo(
        repo_url=config.inputs_url,
        dest_dir=str(config.inputs_dir)
    )

def setup_solutions(config):
    for username in config.users:
        logging.info('Syncing solution repo for {}'.format(username))
        gitsync.sync_repo(config.repo_url(username), config.repo(username))

def setup_venvs(config):
    for username in config.users:
        logging.info('Building venv for {}'.format(username))
        build_venv(config.repo(username), config.venv(username))

def build_venv(git_dir, venv_dir):
    venvbuild.create_venv(venv_dir)

    logging.info('Installing solution requirements')
    user_reqs = os.path.join(git_dir, 'requirements.txt')
    venvbuild.pip_install_requirements(venv_dir, user_reqs)

    logging.info('Installing profiler requirements')
    profiler_reqs = 'profiler_requirements.txt'
    venvbuild.pip_install_requirements(venv_dir, profiler_reqs)

def run_profiler(username, config_file):
    original_cwd = Path.cwd()
    py_path = config_file.venv(username) / 'Scripts' / 'python.exe'
    cmd = [str(py_path), str(original_cwd / 'prof.py')]
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
    os.chdir(config_file.repo(username))
    subprocess.run(cmd)
    os.chdir(original_cwd)

@click.command()
@click.option('--config_path', help='users.yaml file')
def from_user_config(config_path):
    logging.info('Configuring benchmark platform with {}'.format(config_path))
    cfg = config.Config(config_path)
    setup_input_repo(cfg)
    setup_solutions(cfg)
    setup_venvs(cfg)

    for username in cfg.users:
        logging.info(' Profiling {} '.format(username).center(100, '='))
        run_profiler(username, cfg)

    OUTFILE = '2018 comparison.png' #TODO
    plots = compare.plot_comparison(config_path, OUTFILE)
    os.startfile(plots)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from_user_config()