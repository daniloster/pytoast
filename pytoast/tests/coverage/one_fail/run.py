from pytoast import run
from pytoast.decorators import hook
from pytoast.tests.coverage.one_fail.steps import getting_started


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
    run()
