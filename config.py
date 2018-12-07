from pathlib import Path
import yaml

class Config:
    def __init__(self, path):
        self.load(path)

    def load(self, path):
        if isinstance(path, str):
            path = Path(path)
        assert isinstance(path, Path), 'path must be able to be turned into a Path object'
        self._path = path.resolve()
        self.yaml = yaml.load(open(path, 'r'))

        self.res_filename = self.yaml.get('res_filename', 'res.pickle')
        self.timeout = self.yaml.get('timeout', 1000)
        self.working_dir = self.yaml['working_dir']
        self.inputs_url = self.yaml['input']['repo_url']
        self.inputs_dir = self.working_dir / self.yaml['input']['repo_local']

        self.users = self.yaml['users']

    def abs_path(self, path):
        if isinstance(path, str):
            path = Path(path)
        if path.is_absolute():
            return path
        else:
            return path.resolve()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self.load(path)

    @property
    def working_dir(self):
        return self._working_dir

    @working_dir.setter
    def working_dir(self, path):
        self._working_dir = self.abs_path(path)

    @property
    def inputs_dir(self):
        return self._inputs_dir

    @inputs_dir.setter
    def inputs_dir(self, path):
        self._inputs_dir = self.abs_path(path)

    def repo_url(self, username):
        return self.users[username]['repo_url']

    def repo(self, username):
        return self.users[username].get('repo_local', self.working_dir / '{}_repo'.format(username))

    def venv(self, username):
        return self.users[username].get('venv', self.working_dir / '{}_venv'.format(username))

    def results(self, username):
        dir = self.users[username].get('results', self.working_dir / '{}_res'.format(username))
        if not dir.exists():
            dir.mkdir()
        return dir

