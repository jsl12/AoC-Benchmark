import virtualenv
import os
import logging
import subprocess

logging.basicConfig(level=logging.DEBUG)

def create_venv(path):
    #return venv.create(path, with_pip=True)
    virtualenv.create_environment(path)
    # with open(os.path.join(path, 'scripts', 'activate_this.py')) as source_file:
    #     exec(source_file.read())
    #
    # import site;
    # logging.debug(site.getsitepackages())


def pip_install_requirements(venv_path, requirements):
    cmd = [os.path.join(venv_path, 'Scripts', 'pip.exe'), 'install', '-r', requirements]
    subprocess.run(cmd)

if __name__ == "__main__":
    PATH = os.path.join(os.getcwd(), 'repo_venv')
    create_venv(PATH)
    pip_install_requirements(PATH, os.path.join(os.getcwd(), 'requirements.txt')) #TODO
