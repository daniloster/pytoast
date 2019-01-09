from pytoast.decorators import step


@step('^I have given passed$')
def i_have_given_passed_step():
    pass


@step('^I pass by when$')
def i_pass_by_when_step():
    pass


@step('^should be passed (?P<name>(\w+))$')
def should_be_passed_step(name=''):
    assert name in ['Leticia'], 'Incorrect name "{}"'.format(name)
