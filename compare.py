import results as rs
import statplot
import matplotlib.pyplot as plt
import pandas as pd

def single_comparison(key, results):
    fig, ax = plt.subplots(figsize=(19.2, 10.8))
    plt.subplots_adjust(
        top=.95,
        bottom=.05,
        right=.97,
        left=.05
    )
    compare(ax, results, key)
    ax.set_ylabel('Execution Time [ms]')

def compare_multiple(results, fig_path=None):
    common = rs.find_common_solutions(results)
    fig, axes = plt.subplots(nrows=len(common), figsize=(19.2, 5 * len(common)))
    plt.subplots_adjust(
        top=.95,
        bottom=.05,
        right=.97,
        left=.05
    )
    for i, sol in enumerate(sorted(common)):
        compare(axes[i], results, sol)
    if fig_path is not None:
        fig.savefig(fig_path)
    else:
        return fig

def compare(ax, results, key):
    df = pd.DataFrame({user: results[user][key] for user in results})
    ax.set_title(key)
    ax.plot(df, '.')
    ax.grid(True)
    ax.legend(['{} ({:.1f} ms)'.format(user, results[user][key].mean()) for user in results])
    if df.max().max() > ax.get_ylim()[1]:
        statplot.auto_size_y(ax, df)
    ax.set_xlim(0, ax.get_xlim()[1])