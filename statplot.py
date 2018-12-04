import matplotlib.pyplot as plt

def stat_plot(df, res_path='stats.png'):
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

    fig.savefig(res_path)
    print('Saved {}'.format(res_path))
    plt.close(fig)

def auto_size_y(ax, df):
    sizes = [5000, 1000, 500, 250, 100, 50, 10]
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

if __name__ == '__main__':
    from stats import collect_dataframe
    from register import REGISTRATION
    from pathlib import Path

    start, df = collect_dataframe(
        REGISTRATION[-1],
        Path(r'C:\Users\lanca_000\Documents\Software\Python\AoC Benchmark\AoC-Inputs'),
        100
    )
    stat_plot(df)