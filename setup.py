from setuptools import setup

setup(
    name='pytoast',
    version='0.0.2',
    description='A BDD test framework',
    long_description='A BDD test framework with simplicity to use it.',
    license='MIT',
    packages=['pytoast', 'pytoast.decorators', 'pytoast.settings'],
    author='Danilo Castro',
    author_email='daniloster@gmail.com',
    keywords=['bdd', 'framework', 'test', 'py'],
    url='https://github.com/daniloster/pytoast',
    project_urls={
        'Documentation': 'https://github.com/daniloster/pytoast/',
        'Source': 'https://github.com/daniloster/pytoast/',
        'Tracker': 'https://github.com/daniloster/pytoast/issues',
    },
)
