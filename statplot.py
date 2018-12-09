import matplotlib.pyplot as plt
import stats
import click
import sys
from pathlib import Path
import pandas as pd

# Globally ups the dpi when a figure gets saved
plt.rc('savefig', dpi=600)

@click.command()
@click.option('-ip', '--input_path', type=click.Path(exists=True), required=True)
@click.option('-sp', '--sol_path', type=click.Path(exists=True), required=True)
@click.option('-n', '--num', type=int, default=100)
@click.option('-s', '--func_select', type=int, default=-1)
@click.option('-fp', '--fig_path', type=click.Path(), default=None)
def click_collect_and_plot(*args, **kwargs):
    collect_and_plot(*args, **kwargs)

def collect_and_plot(input_path, sol_path, num, func_select, fig_path=None):
    sys.path.insert(0, str(sol_path))
    from register import REGISTRATION
    sys.path.pop(0)

    df = stats.collect_dataframe(
        input_path=input_path,
        sol_path=sol_path,
        num=num,
        func_select=func_select
    )
    fig = stat_plot(df, fig_path, save=False)
    add_func_title(fig.axes[0], REGISTRATION[func_select][1])
    if fig_path is None:
        fig_path = 'results\{}.{}_n{}'.format(
            REGISTRATION[func_select][1].__module__,
            REGISTRATION[func_select][1].__name__,
            num
        ).replace('.', '-') + '.png'
    fig.savefig(fig_path)
    print('Saved to:\n{}'.format(fig_path))
    plt.close(fig)

def load_and_plot(load_path, save=False, close=False):
    # Loads a DataFrame from the CSV at the load_path, which can be either a string
    # or a Path object. It also has the option to save, in which case a PNG file is
    # created with the same stem as the original CSV file in the same location.

    # Assures correct input
    if isinstance(load_path, str):
        try:
            load_path = Path(load_path)
        except:
            print('Could not make a Path object from string')
            raise
    else:
        assert isinstance(load_path, Path), 'load_path must be a Path object or a string that can be made into one'
    assert load_path.exists(), 'load_path must exist'
    assert load_path.suffix == '.csv', 'load_path must point to a CSV file'


    df = pd.read_csv(load_path)
    df = df.set_index(df.columns[0])

    fig = stat_plot(df, save=False)
    fig.axes[0].set_title(load_path.stem.replace('-', ' '))

    if save:
        fig.savefig(load_path.parents[0] / (load_path.stem + '_n{}.png'.format(df.count()[0])))

    # This is helpful if you're going to be making a lot of plots in a row
    if close:
        plt.close(fig)
    else:
        return fig

def stat_plot(df, fig_path='stats.png', save=True):
    plt.rc('font', size=14)
    fig, ax = plt.subplots(figsize=(19.2, 10.8))
    plt.subplots_adjust(
        top=.95,
        bottom=.05,
        right=.97,
        left=.05
    )
    ax.grid(True)

    ax.plot(df, '.')
    add_std_lines(ax, df)

    ax.set_ylabel(df.columns[0])
    auto_size_y(ax, df)

    ax.set_xlim(0, ax.get_xlim()[1])

    add_report_box(ax, df)

    if save:
        fig.savefig(fig_path)
        print('Saved {}'.format(fig_path))
        plt.close(fig)
    else:
        return fig

def auto_size_y(ax, df):
    sizes = [10000, 7500, 5000, 2500, 1000, 500, 250, 100, 50, 10, 5, 2, 1]
    max_val = df.max()[0]
    for i, s in enumerate(sizes[1:]):
        if max_val > s:
            ax.set_ylim(0, sizes[i])
            return

def add_std_lines(ax, df):
    mean = df.mean()[0]
    std = df.std()[0]

    new_mean = df[df < (mean + std)].mean()[0]

    ax.axhline(mean, color='r')
    ax.axhline(new_mean, color='g')
    ax.axhline(mean + std, color='r', linestyle='--')
    ax.axhline(mean - std, color='r', linestyle='--')

def add_report_box(ax, df):
    ax.text(
        .02, .95,
        '{} runs\n{:.1f} ms avg'.format(df.index.size, df.mean()[0]),
        transform=ax.transAxes
    )

def add_func_title(ax, func):
    ax.set_title('{}.{}'.format(
        func.__module__,
        func.__name__
    ))

if __name__ == '__main__':
    click_collect_and_plot()