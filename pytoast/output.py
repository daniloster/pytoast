from termcolor import colored
import click
# from termcolor import colored, cprint
tabs = []


def inc_indent():
    global tabs
    tabs.append('   ')


def dec_indent():
    global tabs
    tabs.pop()


def get_indent():
    return ''.join(tabs)


def reset_indent():
    global tabs
    tabs = []


def get_error(text):
    return c(text, 'red', attrs=['bold'])


def get_warn(text):
    return c(text, 'yellow', attrs=[])


def get_success(text):
    return c(text, 'green', attrs=[])


def c(text, color, attrs=[]):
    return colored(text, color, attrs=[])


def error(text):
    write(get_error(text))


def warn(text):
    write(get_warn(text))


def success(text):
    write(get_success(text))


def write(text):
    click.echo(''.join(tabs) + text)


def write_raw(text):
    click.echo(text)


def br():
    click.echo('')
