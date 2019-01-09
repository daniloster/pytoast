import unittest
from unittest import mock
from unittest.mock import patch
import io
from pytoast import runner
from pytoast.decorators import step, collect_steps


class TestStepDecorator(unittest.TestCase):

    def setUp(self):
        runner.clear()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_collect_all_step_definitions(self, mock_stdout):
        user_name = None
        greeting = None

        @step('^I have created a user named "(?P<name>(\w+))"$')
        def i_have_created_a_user(name):
            user_name = name

        @step('^I am greeted$')
        def i_am_greeted():
            greeting = 'My name is {}'.format(user_name)

        @step('^I should have been greeted as "(?P<name>(\w+))"$')
        def i_should_have_been_greeted_as_name(name):
            local_greeting = 'My name is {}'.format(name)
            assert local_greeting == greeting, '\
            Greeting does not match, found: "{}", expected: "{}"\
            '.format(local_greeting, greeting)

        assert len(runner.steps) == 0, 'There should be not step definition until \
        steps are collected'

        collect_steps(runner)

        assert len(runner.steps) == 3, 'There should be 3 step definitions'

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_collect_empty_step(self, mock_stdout):
        try:

            @step()
            def i_have_created_a_user(name):
                return None

            collect_steps(runner)
            assert False, 'runner should not collect the step without expression'
        except RuntimeError as e:
            message = 'A step must have a match expression'
            assert str(
                e) == message, 'Incorrect exception when colleting step without expression'


if __name__ == '__main__':
    unittest.main()
