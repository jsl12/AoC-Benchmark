from pathlib import Path
import pandas as pd
from memory_profiler import memory_usage
import cProfile
import pstats
import sys

def profile_repo(repo_path, n=3):
    # repo_path should be a Path object and needs to have register.py in the root directory

    sys.path.insert(0, str(repo_path))
    from register import REGISTRATION
    sys.path.pop(0)

    res = {}
    for day in REGISTRATION:
        print('Profiling {}...'.format(day))

        res[day] = {}

        DUT = REGISTRATION[day]

        input = get_input(1)

        res[day]['Memory'] = []
        res[day]['Time'] = []
        for i in range(n):
            res[day]['Memory'].append(memory_usage((DUT,(),{'input': input}), max_usage=True)[0])
            cProfile.runctx('DUT(input)', globals=globals(), locals=locals(), filename='cstats')
            stats = pstats.Stats('cstats')
            res[day]['Time'].append(extract_time(stats, DUT))

    return res

def get_input(day):
    glob = 'day{}*.txt'.format(day)
    file = [f for f in Path(r'C:\Users\lanca_000\Documents\Software\Python\Practice\Advent of Code\2017').glob(glob)][0]
    with open(file, 'r') as f:
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
    # prof = profile_repo(Path(r'C:\Users\lanca_000\Documents\Software\Python\Practice\Advent of Code'))
    prof = profile_repo(Path(r'Q:\AOC\Solutions'))
    print(prof)
