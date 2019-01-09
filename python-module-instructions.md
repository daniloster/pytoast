Since nobody did cover this question of the OP yet:

What I wanted to do:

Make a python module install-able with "pip install ..."

Here is an absolute minimal example, showing the basic steps of preparing and uploading your package to PyPI using setuptools and twine.

This is by no means a substitute for reading at least the tutorial, there is much more to it than covered in this very basic example.

Creating the package itself is already covered by other answers here, so let us assume we have that step covered and our project structure like this:

.
└── hellostackoverflow/
├── **init**.py
└── hellostackoverflow.py
In order to use setuptools for packaging, we need to add a file setup.py, this goes into the root folder of our project:

.
├── setup.py
└── hellostackoverflow/
├── **init**.py
└── hellostackoverflow.py
At the minimum, we specify the metadata for our package, our setup.py would look like this:

from setuptools import setup

setup(
name='hellostackoverflow',
version='0.0.1',
description='a pip-installable package example',
license='MIT',
packages=['hellostackoverflow'],
author='Benjamin Gerfelder',
author_email='benjamin.gerfelder@gmail.com',
keywords=['example'],
url='https://github.com/bgse/hellostackoverflow'
)
Since we have set license='MIT', we include a copy in our project as LICENCE.txt, alongside a readme file in reStructuredText as README.rst:

.
├── LICENCE.txt
├── README.rst
├── setup.py
└── hellostackoverflow/
├── **init**.py
└── hellostackoverflow.py
At this point, we are ready to go to start packaging using setuptools, if we do not have it already installed, we can install it with pip:

pip install setuptools
In order to do that and create a source distribution, at our project root folder we call our setup.py from the command line, specifying we want sdist:

python setup.py sdist
This will create our distribution package and egg-info, and result in a folder structure like this, with our package in dist:

.
├── dist/
├── hellostackoverflow.egg-info/
├── LICENCE.txt
├── README.rst
├── setup.py
└── hellostackoverflow/
├── **init**.py
└── hellostackoverflow.py
At this point, we have a package we can install using pip, so from our project root (assuming you have all the naming like in this example):

pip install ./dist/hellostackoverflow-0.0.1.tar.gz
If all goes well, we can now open a Python interpreter, I would say somewhere outside our project directory to avoid any confusion, and try to use our shiny new package:

Python 3.5.2 (default, Sep 14 2017, 22:51:06)
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.

> > > from hellostackoverflow import hellostackoverflow
> > > hellostackoverflow.greeting()
> > > 'Hello Stack Overflow!'
> > > Now that we have confirmed the package installs and works, we can upload it to PyPI.

Since we do not want to pollute the live repository with our experiments, we create an account for the testing repository, and install twine for the upload process:

pip install twine
Now we're almost there, with our account created we simply tell twine to upload our package, it will ask for our credentials and upload our package to the specified repository:

twine upload --repository-url https://test.pypi.org/legacy/ dist/\*
We can now log into our account on the PyPI test repository and marvel at our freshly uploaded package for a while, and then grab it using pip:

pip install --index-url https://test.pypi.org/simple/ hellostackoverflow
As we can see, the basic process is not very complicated. As I said earlier, there is a lot more to it than covered here, so go ahead and read the tutorial for more in-depth explanation.
