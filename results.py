from pathlib import Path
from config import Config
import pickle
import pandas as pd

def load_results(config_file, username):
    assert isinstance(username, list) or isinstance(username, str)

    if not isinstance(config_file, Config):
        cfg = Config(config_file)
    else:
        cfg = config_file

    if isinstance(username, list):
        res = {}
        for u in username:
            res[u] = make_df(pickle.load(open(cfg.results(u), 'rb')))
        return res
    elif isinstance(username, str):
        if username in cfg.users:
            return make_df(pickle.load(open(cfg.results(username), 'rb')))
        else:
            print('User {} not found in {}'.format(username, cfg.path.name))

def make_df(results):
    return pd.DataFrame({res[0]: res[1]['Time'] for res in results})

def find_common_solutions(config):
    if isinstance(config, Config):
        cfg = config
    elif isinstance(config, str):
        cfg = Config(config)
    else:
        print('Not found')

    results = load_results(config, [user for user in cfg.users])
    cmd = 'global res; res = list({})'.format(' & '.join(['set(results[\'{}\'])'.format(user) for user in cfg.users]))
    exec(cmd)
    return res

if __name__ == '__main__':
    res2 = load_results('users.yaml', ['John', 'Shahvir'])
    common = find_common_solutions('users.yaml')
    print(common)
    # res = load_results('users.yaml', 'John')
    # print(res)
