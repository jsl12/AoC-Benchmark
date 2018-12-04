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
    end = datetime.now()
    print('Elapsed time: {}'.format(end - start))
    return res

@click.command()
@click.option('-ip', '--input_path', type=click.Path(exists=True), required=True)
@click.option('-sp', '--sol_path', type=click.Path(exists=True), required=True)
@click.option('-csv', '--csv_path', type=click.Path(), default='stats.csv')
@click.option('-n', type=int, default=100)
@click.option('-s', type=int, default=-1)
def collect_dataframe(input_path, sol_path, s, n, csv_path):
    sys.path.insert(0, str(sol_path))
    from register import REGISTRATION
    sys.path.pop(0)

    res = collect_stats(
        REGISTRATION[s],
        input_path,
        n
    )
    df = pd.DataFrame(res, columns=['Execution Duration [ms]'])
    df.index.name = 'Run #'
    return df

if __name__ == '__main__':
    collect_dataframe()