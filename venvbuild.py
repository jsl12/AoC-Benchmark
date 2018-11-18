import virtualenv
import os
import logging
import subprocess


def create_venv(path):
    virtualenv.create_environment(path)


def pip_install_requirements(venv_path, requirements):
    cmd = [os.path.join(venv_path, 'Scripts', 'pip.exe'), 'install', '-r', requirements]
    subprocess.run(cmd)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    PATH = os.path.join(os.getcwd(), 'repo_venv')
    create_venv(PATH)
    pip_install_requirements(PATH, os.path.join(os.getcwd(), 'requirements.txt')) #TODO
