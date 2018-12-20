import git
from pathlib import Path
import logging


def sync_repo(repo_url, dest_dir, branch='master', remote='origin'):
    # convert to Path object if it isn't already
    if not isinstance(dest_dir, Path):
        dest_dir = Path(dest_dir)

    # Creates the instance of the Repo object
    try:
        logging.info('Attempting to create repo from {}'.format(dest_dir))
        repo = git.Repo(dest_dir)
    except (git.InvalidGitRepositoryError, git.NoSuchPathError) as e:
        logging.info('Creating repository at {}'.format(dest_dir))
        repo = git.Repo.init(dest_dir)

    # Makes sure there's a remote with the right name and fetches the data
    try:
        origin = repo.remotes[remote]
    except IndexError as e:
        origin = repo.create_remote(remote, repo_url)
    origin.fetch()

    # Makes sure the remote has a branch with the right name
    try:
        origin.refs[branch]
    except IndexError as e:
        print('Branch \'{}\' not found on remote \'{}\''.format(branch, remote))
        raise

    # Makes sure there's a local branch with the right name
    try:
        head = repo.heads[branch]
    except IndexError as e:
        head = repo.create_head(branch, origin.refs[branch])

    # Make sure it's tracking the correct remote branch
    if head.tracking_branch() != origin.refs[branch]:
        head.set_tracking_branch(origin.refs[branch])

    head.checkout()
    info = origin.pull()

    return repo.working_dir

if __name__ == "__main__":
    import config
    logging.basicConfig(level=logging.INFO)
    REPO_URL = 'https://github.com/jsl12/AoC-Solutions'
    PATH = config.Config(Path('users.yaml')).working_dir / 'test_sync'
    sync_repo(REPO_URL, PATH)