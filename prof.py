from pathlib import Path
import cProfile
import pstats
import sys
import pickle

import click
import pandas as pd
from memory_profiler import memory_usage

INPUT_PATH = Path(r'C:\Users\lanca_000\Documents\Software\Python\Practice\Advent of Code\2017')


@click.command()
@click.option('--repo_path', type=Path, required=True, help='Path to register.py')
@click.option('--input_path', type=Path, required=True, help='Path to folder containing input files. glob: \'day*{}*.txt\'')
@click.option('--n', default=100, help='Number of times to run during the time profile')
def profile_repo(repo_path, input_path, n=5):
    # repo_path should be a Path object and needs to have register.py in the root directory

    sys.path.insert(0, str(repo_path))
    from register import REGISTRATION
    sys.path.pop(0)

    res = {}
    for day in REGISTRATION:
        # print('Starting profile of {}'.format(day))
        print(' {} '.format(day).center(50, '='))

        res[day] = {}

        DUT = REGISTRATION[day]
        print('Registered solution function: {}.{}'.format(DUT.__module__, DUT.__name__))

        input = get_input(1)

        print('Assessing memory usage...')
        res[day]['Memory'] = memory_usage((DUT, (), {'input': input}), max_usage=True)[0]
        print('{:.2f} MB'.format(res[day]['Memory']))

        print('Starting {} runs...'.format(n))
        res[day]['Time'] = [None for i in range(n)]
        total_time = 0
        for i in range(n):
            cProfile.runctx('DUT(input)', globals=globals(), locals=locals(), filename='cstats')
            stats = pstats.Stats('cstats')
            t = extract_time(stats, DUT)
            total_time += t
            res[day]['Time'][i] = t
        avg_time = total_time / n
        print('{:.1f} ms average'.format(avg_time))

    return res

def get_input(day):
    glob = 'day*{}*.txt'.format(day)
    file = [f for f in INPUT_PATH.glob(glob)][0]
    with open(file, 'r') as f:
        print('Getting input from {}'.format(file.name))
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
    with open('res.pickle', 'wb') as file:
        pickle.dump(profile_repo(), file)