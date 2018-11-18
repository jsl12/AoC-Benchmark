import gitsync
import venvbuild
import os
import configparser
import click

def build_env(giturl, git_dir, venv_dir):
    gitsync.sync_repo(giturl, git_dir)
    venvbuild.create_venv(venv_dir)
    user_reqs = os.path.join(git_dir, 'requirements.txt')
    if os.path.isfile(user_reqs):
        logging.info('Installing from {}'.format(user_reqs))
        venvbuild.pip_install_requirements(venv_dir, user_reqs)


@click.command()
@click.option('--users', help='users.ini file')
def from_users_ini(users):
    cfg = configparser.ConfigParser()
    cfg.read(users)
    for user in cfg.sections():
        git_path = user + '_repo'
        venv_path = user + '_venv'
        build_env(cfg[user]['REPO_URL'], git_path, venv_path)


if __name__ == "__main__":
    from_users_ini()