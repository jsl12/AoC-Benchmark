from pathlib import Path
from config import Config
import pickle

def load_results(config_file, username):
    assert isinstance(config_file, Path) or isinstance(config_file, str)
    assert isinstance(username, list) or isinstance(username, str)
    cfg = Config(config_file)
    if isinstance(username, list):
        res = {}
        for u in username:
            res[u] = pickle.load(open(cfg.results(u), 'rb'))
        return res
    elif isinstance(username, str):
        if username in cfg.users:
            return pickle.load(open(cfg.results(username), 'rb'))
        else:
            print('User {} not found in {}'.format(username, cfg.path.name))

def get_solutions(results):
    return [sol[0] for sol in results]

def find_common_solutions(results):
    sols = [get_solutions(results[user]) for user in results]
    cmd = ['set(sols[{}])'.format(i) for i, lis in enumerate(sols)]
    cmd = 'res = list({})'.format(' & '.join(cmd))
    exec(cmd)
    if len(res) > 0:
        return res

if __name__ == '__main__':
    res = load_results('users.yaml', ['John', 'Shahvir'])
    find_common_solutions(res)
    print(res)
