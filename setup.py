import os
from setuptools import setup

# The directory containing this file
README_PATH = os.path.abspath(os.path.dirname(__file__))
README_PATH = os.path.join(README_PATH, 'README.md')

with open(README_PATH, 'r') as file:
    README = file.read()

setup(
    name='pytoast',
    version='0.0.4',
    description='A BDD test framework',
    long_description=README,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=['pytoast', 'pytoast.decorators', 'pytoast.settings'],
    author='Danilo Castro',
    author_email='daniloster@gmail.com',
    keywords=['bdd', 'framework', 'test', 'py'],
    url='https://github.com/daniloster/pytoast',
    project_urls={
        'Source': 'https://github.com/daniloster/pytoast/',
        'Tracker': 'https://github.com/daniloster/pytoast/issues',
    },
)
