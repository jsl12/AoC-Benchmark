from config import Config
import pickle
import pandas as pd

def load_results(config_file, username=None):
    if not isinstance(config_file, Config):
        cfg = Config(config_file)
    else:
        cfg = config_file

    if username is None:
        res = {}
        for u in cfg.users:
            res[u] = make_df(pickle.load(open(cfg.results(u), 'rb')))
        return res
    elif isinstance(username, str):
        if username in cfg.users:
            return make_df(pickle.load(open(cfg.results(username), 'rb')))
        else:
            print('User {} not found in {}'.format(username, cfg.path.name))

def make_df(results):
    return pd.DataFrame({res[0]: res[1]['Time'] for res in results})

def find_common_solutions(results):
    cmd = 'global res; res = list({})'.format(' & '.join(['set(results[\'{}\'])'.format(user) for user in results]))
    exec(cmd)
    return res

if __name__ == '__main__':
    res2 = load_results('users.yaml')
    common = find_common_solutions(res2)
    print(common)
    # res = load_results('users.yaml', 'John')
    # print(res)
