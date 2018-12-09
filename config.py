from pathlib import Path
import yaml

class Config:
    def __init__(self, path):
        self.load(path)

    def load(self, yaml_path):
        if isinstance(yaml_path, str):
            yaml_path = Path(yaml_path)
        assert isinstance(yaml_path, Path), 'path must be able to be turned into a Path object'
        self.path = yaml_path.resolve()
        self.yaml = yaml.load(open(yaml_path, 'r'))

        self.working_dir = Path(self.yaml['working_dir'])
        if not self.working_dir.is_absolute():
            self.working_dir = self.path.parents[0] / self.working_dir
        self.res_filename = self.yaml.get('res_filename', 'res.pickle')
        self.timeout = self.yaml.get('timeout', -1)
        self.inputs_url = self.yaml['input']['repo_url']
        self.inputs_dir = self.working_dir / self.yaml['input']['repo_local']
        self.users = self.yaml['users']

    def repo_url(self, username):
        return self.users[username]['repo_url']

    def _abs(self, dir):
        if isinstance(dir, str):
            dir = Path(dir)
        if not dir.is_absolute():
            return self.working_dir / dir
        else:
            return dir

    def repo(self, username):
        return self._abs(self.users[username].get('repo_local', '{}_repo'.format(username)))

    def venv(self, username):
        return self._abs(self.users[username].get('venv', '{}_venv'.format(username)))

    def results(self, username):
        dir = self._abs(self.users[username].get('results', '{}_res'.format(username)))
        if not dir.exists():
            dir.mkdir()
        return dir / self.res_filename

