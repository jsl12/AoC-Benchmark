import git
from pathlib import Path
import logging


def sync_repo(repo_url, dest_dir, branch='master', remote='origin'):
    # convert to Path object if it isn't already
    if not isinstance(dest_dir, Path):
        dest_dir = Path(dest_dir)

    # check to see if directory already exists. If it doesn't, then we can clone into it no problem
    if not dest_dir.exists():
        logging.info('Directory not found: {}'.format(dest_dir))
        logging.info('Cloning from {}'.format(repo_url))
        repo = git.Repo.clone_from(repo_url, dest_dir, branch=branch)
    else:
        try:
            logging.info('Attempting to create repo from {}'.format(dest_dir))
            repo = git.Repo(dest_dir)
        except git.InvalidGitRepositoryError as e:
            logging.info('Could not make repo from {}'.format(dest_dir))
            repo = git.Repo.init(dest_dir)

        if remote not in repo.remotes:
            repo.create_remote(remote, repo_url)

    # Should have a repo setup by now, no matter what
    info = repo.remotes[remote].pull()

    # try:
    #
    #     repo = git.Repo.clone_from(repo_url, dest_dir, branch='master')
    # except git.exc.GitCommandError as e:
    #     if e.status == 128:
    #         logging.info('   Syncing {} to {}'.format(repo_url, dest_dir))
    #         g = git.cmd.Git(dest_dir)
    #         g.pull()
    #         #TODO get this working
    #         return None
    return repo.working_dir


if __name__ == "__main__":
    import config
    logging.basicConfig(level=logging.DEBUG)
    REPO_URL = 'https://github.com/jsl12/AoC-Solutions'
    PATH = config.Config(Path('users.yaml')).working_dir / 'test_sync'
    sync_repo(REPO_URL, PATH)