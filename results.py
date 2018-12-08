from pathlib import Path
from config import Config
import pickle
import pandas as pd

def load_results(config_file, username):
    assert isinstance(config_file, Path) or isinstance(config_file, str)
    assert isinstance(username, list) or isinstance(username, str)
    cfg = Config(config_file)
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

if __name__ == '__main__':
    res = load_results('users.yaml', ['John', 'Shahvir'])
    # res = load_results('users.yaml', 'John')
    print(res)
