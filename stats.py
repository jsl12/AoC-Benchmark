import cProfile
import pstats
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import prof
import click

def collect_stats(solution, input_path, n=1000):
    print('Collecting stats on:\n{}.{}'.format(solution[1].__module__, solution[1].__name__))
    print('{} runs'.format(n))
    input = prof.get_input(solution[0], input_path)
    res = np.empty(n)
    start = datetime.now()
    for i in range(n):
        cProfile.runctx('solution[1](input)', globals=globals(), locals=locals(), filename='cstats')
        stats = pstats.Stats('cstats')
        t = prof.extract_time(stats, solution[1])
        res[i] = t
        print('Run {} {:.1f} ms'.format(i, t))
    end = datetime.now()
    print('Elapsed time: {}'.format(end - start))
    return res

@click.command()
@click.option('-ip', '--input_path', type=click.Path(exists=True), required=True)
@click.option('-sp', '--sol_path', type=click.Path(exists=True), required=True)
@click.option('-csv', '--csv_path', type=click.Path(), default=None)
@click.option('-s', '--func_select', type=int, default=-1)
@click.option('-n', '--num', type=int, default=100)
def collect_dataframe(input_path, sol_path, csv_path, func_select, num):
    sys.path.insert(0, str(sol_path))
    from register import REGISTRATION
    sys.path.pop(0)

    res = collect_stats(
        REGISTRATION[func_select],
        input_path,
        num
    )
    df = pd.DataFrame(res, columns=['Execution Duration [ms]'])
    df.index.name = 'Run #'
    if csv_path is not None:
        df.to_csv(csv_path)
    return df

if __name__ == '__main__':
    collect_dataframe()