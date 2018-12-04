import matplotlib.pyplot as plt

def stat_plot(df, res_path='stats.png'):
    fig, ax = plt.subplots(figsize=(19.2, 10.8))
    ax.plot(df, '.')
    ax.grid(True)
    ax.set_ylabel(df.columns[0])

    max_val = df.max()[0]
    if  max_val > 1000:
        x_max = 5000
    elif max_val > 500:
        x_max = 1000
    elif max_val > 250:
        x_max = 500
    elif max_val > 100:
        x_max = 250
    elif max_val > 50:
        x_max = 100
    ax.set_ylim(0, x_max)

    ax.set_xlim(0, df.index[-1])

    fig.savefig(res_path)
    plt.close(fig)

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