from config import Config
import pickle
import pandas as pd
import numpy as np
import fasteners

def dump_results(path, results):
    with fasteners.InterProcessLock(path.with_suffix('.lock')):
        with open(path, 'wb') as file:
            print('Saving results for {} solutions to {}/{}'.format(len(results), path.parents[0].name, path.name))
            pickle.dump(results, file)

def load_results(config_file, username=None):
    if not isinstance(config_file, Config):
        cfg = Config(config_file)
    else:
        cfg = config_file

    if username is None:
        res = {}
        for u in cfg.users:
            with fasteners.InterProcessLock(cfg.results(u).with_suffix('.lock')):
                res[u] = make_df(pickle.load(open(cfg.results(u), 'rb')))
        return res
    elif isinstance(username, str):
        if username in cfg.users:
            with fasteners.InterProcessLock(cfg.results(username).with_suffix('.lock')):
                return make_df(pickle.load(open(cfg.results(username), 'rb')))
        else:
            print('User {} not found in {}'.format(username, cfg.path.name))

def make_df(results):
    res = pd.DataFrame(index=pd.Index(np.arange(max(len(values['Time']) for id, values in results))))
    for id, values in results:
        vals = np.full(len(res.index), np.nan)
        vals [:values['Time'].size] = values['Time'][:]
        res[id] = vals
    return res

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
