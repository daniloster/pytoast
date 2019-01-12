# pytoast

A simple BDD (Behaviour-Driven Development) framework to run tests by CLI. The motivation came from some problems trying to make other test frameworks work in a simple way for different environment configurations.

Version: [pytoast](https://pypi.org/project/pytoast/)

#### `Python >= 3.3.x`

There were a few issues to support `python@2.7.x`, then, it has been drop.

## Installing

### By requirements.txt

You may get the latest version by setting this inside the requirements file

```
pytoast
```

Or specific version

```
pytoast==version_number
```

### By pip

```sh
pip install pytoast
```

## Usage

To use this module for testing is pretty simple. First you need to create you entrypoint python file which can be named as you wish. For instance, lets call it `run_tests.py`.

### Test entrypoint

> \${root}/run_tests.py

```python
from pytoast import run
from pytoast import hook
# "tests" is your folder with the step definitions
from tests import getting_started

# That is how you add a hooks and they are only
# before_all, before_each, after_each and after_all
@hook(event="before_all")
def setting_up_before_all():
    print('before_all')


@hook(event="before_each")
def setting_up_before_each():
    print('before_each')


@hook(event="after_all")
def setting_up_after_all():
    print('after_all')


@hook(event="after_each")
def setting_up_after_each():
    print('after_each')


if __name__ == '__main__':
    # Executing run in this file you are invoking the
    # entrypoint to the test execution, this will be fine
    # if you have imported all your step definitions e.g.
    # our `getting_started.py`. Step definitions are global
    # and may be reused in different `*.feature` files.
    run()
```

To get more info, try executing: `python run_tests.py --help`
This will provide you a list of arguments that can/should be set. The mandatory arguments are root and features.
| Argument | Description |
| ---------------- | ------------- |
| `--root` | The root folder path to your project |
| `--features` | The folder path to your ".feature" files |
| `--tags` | It will filter the scenarios that will get executed |
| `--fail-fast` | Define whether the process should abort when a scenario fail |
| `--verbose` | Define whether display stacktrace for errors |

### Feature files

Define your scenarios in a human readable language which step definitions will match against it and perform some tasks/operations.

> \${root}/feature/getting_started.feature

```feature
Scenario: Getting started incorrect
  Given I have given passed
  When I pass by when
  Then should be passed Danilo
  And should be passed Leticia


Scenario: Getting started correct
  Given I have given passed
  When I pass by when
  Then should be passed Leticia
```

### Step definitions

To define a step definition, you will need the `step` decorator which expects a regex as string that will be evaluated against the sentences in the feature files. The keywords `given`, `when`, `then` and `and` are ignored from the beginning of the sentences. So, for the example above `Given I have given passed` we evaluate `I have given passed` against the regex. The first match will run it. For this reason, it is important to set step definitions with `^` and `$`, those define the start and end of the sentence.

> \${root}/tests/getting_started.py

```python
from pytoast import step


@step('^I have given passed$')
def i_have_given_passed_step():
    pass


@step('^I pass by when$')
def i_pass_by_when_step():
    pass


@step('^should be passed (?P<place>(\w+))$')
def should_be_passed_step(place=''):
    assert place == 'Leticia', 'Incorrect place name "{}"'.format(place)

```

### Running

To run you test you will need to invoke python against your tests entrypoint.

`python run_tests.py --root "${pwd}" --features "${pwd}/features" --verbose`

## Requirements

To use this library will need to install the following modules

- click==7.0
- mock==2.0.0
- psycopg2
- setuptools
- termcolor==1.1.0
