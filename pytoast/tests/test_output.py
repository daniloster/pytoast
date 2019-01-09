import unittest
from mock import Mock, patch, call
import click
from pytoast import output


class TestOutput(unittest.TestCase):

    def setUp(self):
        self.mock_print = Mock()
        output.reset_indent()

    def test_simple_write(self):
        with patch('click.echo', self.mock_print):
            output.write('text is printed')
            is_correct = self.mock_print.mock_calls[-1] == call(
                'text is printed')
            assert is_correct, 'Printed text is not correct, found: "{}"'.format(
                self.mock_print.mock_calls[-1]
            )

    def test_indent_increased(self):
        with patch('click.echo', self.mock_print):
            output.inc_indent()
            output.write('text is printed')
            is_correct = self.mock_print.mock_calls[-1] == call(
                '   text is printed')
            assert is_correct, 'Printed text is not correct, found: "{}", {}'.format(
                self.mock_print.mock_calls[-1], call('   text is printed')
            )

    def test_indent_decreased(self):
        with patch('click.echo', self.mock_print):
            output.inc_indent()
            output.inc_indent()
            output.write('text is printed')
            is_correct = self.mock_print.mock_calls[-1] == call(
                '      text is printed')
            assert is_correct, 'Printed text indented inc x2 is not correct, found: "{}"'.format(
                self.mock_print.mock_calls[-1]
            )

            output.dec_indent()
            output.write('text is printed')
            is_correct = self.mock_print.mock_calls[-1] == call(
                '   text is printed')
            assert is_correct, 'Printed text indented dec x1 is not correct, found: "{}"'.format(
                self.mock_print.mock_calls[-1]
            )

    def test_error(self):
        with patch('click.echo', self.mock_print):
            output.error('text is printed')
            is_correct = self.mock_print.mock_calls[-1] == call(
                '\x1b[31mtext is printed\x1b[0m')
            assert is_correct, 'Printed text is not correct, found: "{}"'.format(
                self.mock_print.mock_calls[-1]
            )

    def test_warn(self):
        with patch('click.echo', self.mock_print):
            output.warn('text is printed')
            is_correct = self.mock_print.mock_calls[-1] == call(
                '\x1b[33mtext is printed\x1b[0m')
            assert is_correct, 'Printed text is not correct, found: "{}"'.format(
                self.mock_print.mock_calls[-1]
            )

    def test_success(self):
        with patch('click.echo', self.mock_print):
            output.success('text is printed')
            is_correct = self.mock_print.mock_calls[-1] == call(
                '\x1b[32mtext is printed\x1b[0m')
            assert is_correct, 'Printed text is not correct, found: "{}"'.format(
                self.mock_print.mock_calls[-1]
            )

    def test_br(self):
        with patch('click.echo', self.mock_print):
            output.br()
            is_correct = self.mock_print.mock_calls[-1] == call('')
            assert is_correct, 'Printed text is not correct, found: "{}"'.format(
                self.mock_print.mock_calls[-1]
            )


if __name__ == '__main__':
    unittest.main()
