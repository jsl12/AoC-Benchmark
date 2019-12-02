import cProfile
import pstats
import sys
from pathlib import Path

import click
import numpy as np
from memory_profiler import memory_usage

import results


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
    '-resp',
    '--result_path',
    required=True,
    type=Path,
    help='Path to result file'
)
@click.option(
    '-n',
    type=int,
    default=100,
    show_default=True,
    help='Number of times to run cProfile'
)
@click.option(
    '-to',
    '--timeout',
    type=int,
    default=-1,
    show_default=True,
    help='Timeout in ms. Profiler will try to only run each solution for this long'
)
def profile_repo(repo_path, input_path, result_path, n, timeout):
    """

    :param repo_path: Path object, needs to have register.py in the root directory
    :param input_path: Path object, files should match the glob day*{}*.txt
    :param result_path: Path object,
    :param n: int, number of times to run cProfile
    :param timeout: int, timeout in ms
    :return:
    """
    # repo_path should be a Path object and needs to have register.py in the root directory
    # input path should be a Path object and should have files that match the glob day*{}*.txt
    # n is the number of times to run cProfile

    sys.path.insert(0, str(repo_path))
    from register import REGISTRATION
    sys.path.pop(0)

    cstats = str(result_path.parents[0]  / 'cstats.temp')

    res = []
    n_original = n
    for id, DUT in REGISTRATION:
        # print('Starting profile of {}'.format(day))
        print(' {} '.format(id).center(50, '='))
        print('Registered solution function: {}.{}'.format(DUT.__module__, DUT.__name__))

        input = get_input(id, input_path)

        print('Assessing memory usage...')
        try:
            mem_use = memory_usage((DUT, (), {'input': input}), max_usage=True)[0]
        except Exception as e:
            print(' {} '.format('SOLUTION FAILED').center(50, '*'))
            print(e)
            continue
        print('{:.2f} MB'.format(mem_use))

        print('Initial solution run:')
        cProfile.runctx('DUT(input)', globals=globals(), locals=locals(), filename=cstats)
        stats = pstats.Stats(cstats)
        t = extract_time(stats, DUT)
        print('{:.1f} ms'.format(t))

        if timeout >= 0:
            n_timeout = int((timeout - t) / t)
            if n_timeout < n:
                n = n_timeout
                if n != 0:
                    print('Adjusting to {} runs'.format(n))
        if n == 0:
            print('Not enough time for more runs')
            res.append((id, {'Memory': mem_use, 'Time': np.array([t])}))
        else:
            print('Starting {} runs...'.format(n))
            times = np.empty(n)
            for i in range(n):
                cProfile.runctx('DUT(input)', globals=globals(), locals=locals(), filename=cstats)
                stats = pstats.Stats(cstats)
                times[i] = extract_time(stats, DUT)
            print('{:.1f} ms average'.format(times.mean()))
            res.append((id, {'Memory': mem_use, 'Time': times}))
        n = n_original
        results.dump_results(result_path, res)

    return res

def get_input(id, path):
    id = id.split('.')
    glob = '{}/*day{}*.txt'.format(id[0], id[1])
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

if __name__ == '__main__':
    profile_repo()