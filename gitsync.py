import git
import os
import logging

def sync_repo(repo_url, dest_dir):
    try:
        logging.info('Cloning {} to {}'.format(repo_url, dest_dir))
        repo = git.Repo.clone_from(repo_url, dest_dir, branch='master')
    except git.exc.GitCommandError as e:
        if e.status == 128:
            logging.info('   Syncing {} to {}'.format(repo_url, dest_dir))
            repo = git.Repo.init(dest_dir)
    return repo.working_dir

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    REPO_URL = 'https://github.com/shahvirb/adventOfCode2017'
    PATH = os.path.join(os.getcwd(), 'repo')
    sync_repo(REPO_URL, PATH)