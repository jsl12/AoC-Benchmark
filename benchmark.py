import gitsync
import venvbuild
import os
import configparser
import click
import logging



def build_env(giturl, git_dir, venv_dir):
    gitsync.sync_repo(giturl, git_dir)
    venvbuild.create_venv(venv_dir)

    user_reqs = os.path.join(git_dir, 'requirements.txt')
    venvbuild.pip_install_requirements(venv_dir, user_reqs)

    profiler_reqs = 'profiler_requirements.txt'
    venvbuild.pip_install_requirements(venv_dir, profiler_reqs)


@click.command()
@click.option('--users', help='users.ini file')
def from_users_ini(users):
    cfg = configparser.ConfigParser() #TODO refactor out configparser into a seperate func
    cfg.read(users)
    usernames = [s for s in cfg.sections() if s != 'Config']

    logging.info('Fetching Inputs')
    gitsync.sync_repo(cfg['Config']['INPUT_REPO_URL'].strip(), 'AoC-Inputs')

    for user in usernames:
        logging.info('Building environment for {}')
        git_url = cfg[user]['REPO_URL'].strip()
        git_path = user + '_repo'
        venv_path = user + '_venv'
        build_env(git_url, git_path, venv_path)




if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from_users_ini()