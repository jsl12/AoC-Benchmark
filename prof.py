from pathlib import Path
import cProfile
import pstats
import sys
import pickle

import click
import pandas as pd
import numpy as np
from memory_profiler import memory_usage

import cfg

@click.command()
@click.option(
    '-rp',
    '--repo_path',
    required=True,
    type=Path,
    help='Path containing register.py'
)
@click.option(
    '-ip',
    '--input_path',
    required=True,
    type=Path,
    help='Path to folder containing input files. glob: \'day*{}*.txt\''
)
@click.option(
    '-n',
    type=int,
    default=100,
    show_default=True,
    help='Number of times to run cProfile'
)
@click.option(
    '-uc',
    '--users_config',
    type=Path,
    default='users.yaml',
    show_default=True,
    help='Path to user configuration file'
)
@click.option(
    '-u',
    '--username',
    type=str,
    required=True,
    help='Username to associate with results'
)
@click.option(
    '-to',
    '--timeout',
    type=int,
    default=10000,
    show_default=True,
    help='Timeout in ms. Profiler will try to only run each solution for this long'
)
def profile_repo(repo_path, input_path, n, users_config, username, timeout):
    # repo_path should be a Path object and needs to have register.py in the root directory
    # input path should be a Path object and should have files that match the glob day*{}*.txt
    # n is the number of times to run cProfile

    sys.path.insert(0, str(repo_path))
    from register import REGISTRATION
    sys.path.pop(0)

    res = {}
    for id, DUT in REGISTRATION:
        # print('Starting profile of {}'.format(day))
        print(' {} '.format(id).center(50, '='))

        res[id] = {}

        print('Registered solution function: {}.{}'.format(DUT.__module__, DUT.__name__))

        input = get_input(id, input_path)

        print('Assessing memory usage...')
        res[id]['Memory'] = memory_usage((DUT, (), {'input': input}), max_usage=True)[0]
        print('{:.2f} MB'.format(res[id]['Memory']))

        print('Initial solution run:')
        cProfile.runctx('DUT(input)', globals=globals(), locals=locals(), filename='cstats')
        stats = pstats.Stats('cstats')
        t = extract_time(stats, DUT)
        print('{:.1f} ms'.format(t))

        n_timeout = int((timeout - t) / t)
        if n_timeout < n:
            n = n_timeout
            print('Adjusting to {} runs'.format(n))

        print('Starting {} runs...'.format(n))
        res[id]['Time'] = np.empty(n)
        total_time = 0
        for i in range(n):
            cProfile.runctx('DUT(input)', globals=globals(), locals=locals(), filename='cstats')
            stats = pstats.Stats('cstats')
            t = extract_time(stats, DUT)
            total_time += t
            res[id]['Time'][i] = t
        avg_time = total_time / n
        print('{:.1f} ms average'.format(avg_time))

    with open(cfg.results(users_config, username), 'wb') as file:
        pickle.dump(res, file)

    return res

def get_input(id, path):
    id = id.split('.')
    glob = '{}/*day*{}*.txt'.format(id[0], id[1])
    if isinstance(path, str):
        path = Path(path)
    file = [f for f in path.glob(glob)][0]
    with open(file, 'r') as f:
        print('Getting input from:\n{}'.format(file))
        return f.read()

def extract_time(pstats, func_handle):
    for func in pstats.stats:
        if func_handle.__name__ == func[2]:
            return pstats.stats[func][3] * 1000

def pstats_to_df(stats_obj):
    df = pd.DataFrame({
        'paths': [Path(func[0]) for func in stats_obj.stats],
        'lines': [func[1] for func in stats_obj.stats],
        'func names': [func[2] for func in stats_obj.stats],
        # 'func names': [pstats.func_std_string(func) for func in stats_obj.stats],
        'primitive calls': [stats_obj.stats[func][0] for func in stats_obj.stats],
        'total calls': [stats_obj.stats[func][1] for func in stats_obj.stats],
        'total time': [stats_obj.stats[func][2] * 1000 for func in stats_obj.stats],
        'cumulative time': [stats_obj.stats[func][3] * 1000 for func in stats_obj.stats]
    })

    df['percall total'] = df['total time'] / df['total calls']
    df['percall cumulative'] = df['cumulative time'] / df['primitive calls']
    return df

if __name__ == '__main__':
    profile_repo()