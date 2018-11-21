from setuptools import setup

setup(
    name='AoC Benchmark',
    version='0.1',
    py_modules=['prof'],
    install_requires=[
        'pandas',
        'memory_profiler',
        'Click',
    ],
    entry_points='''
        [console_scripts]
        profile_repo=prof:profile_repo
    ''',
)