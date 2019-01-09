import os
import unittest
from mock import Mock, patch, call
from pytoast.settings.features import Features


class TestOutput(unittest.TestCase):

    def setUp(self):
        self.features = Features()

    @patch('click.echo', new_callable=Mock())
    def test_parse_file(self, mock_print):
        feature_path = os.path.abspath(
            os.path.dirname(__file__) + '/../coverage/all_success/features/getting_started.feature')
        self.features.parse_file(feature_path)
        assert len(
            self.features.scenarios) == 2, 'Expected to parse 2 scenarios from the feature file'

        name = self.features.scenarios[0].name
        tags = self.features.scenarios[0].tags
        steps = self.features.scenarios[0].steps
        first_step = '{} {}'.format(steps[0][0].lower(), steps[0][1])
        second_step = '{} {}'.format(steps[1][0].lower(), steps[1][1])
        third_step = '{} {}'.format(steps[2][0].lower(), steps[2][1])

        assert name == 'Getting started incorrect', 'The first scenario name is incorrect, found "{}"'.format(
            name)
        assert '|'.join(
            tags) == '', 'First scenario tags are incorrect, found "{}"'.format('|'.join(tags))
        assert first_step == 'given I have given passed', 'Given step is not correct, found "{}"'.format(
            first_step)
        assert second_step == 'when I pass by when', 'When step is not correct, found "{}"'.format(
            second_step)
        assert third_step == 'then should be passed Danilo', 'Then step is not correct, found "{}"'.format(
            third_step)

        name = self.features.scenarios[1].name
        tags = self.features.scenarios[1].tags
        steps = self.features.scenarios[1].steps
        first_step = '{} {}'.format(steps[0][0].lower(), steps[0][1])
        second_step = '{} {}'.format(steps[1][0].lower(), steps[1][1])
        third_step = '{} {}'.format(steps[2][0].lower(), steps[2][1])

        assert name == 'Getting started correct', 'The first scenario name is incorrect, found "{}"'.format(
            name)
        assert '|'.join(
            tags) == '', 'First scenario tags are incorrect, found "{}"'.format('|'.join(tags))
        assert first_step == 'given I have given passed', 'Given step is not correct, found "{}"'.format(
            first_step)
        assert second_step == 'when I pass by when', 'When step is not correct, found "{}"'.format(
            second_step)
        assert third_step == 'then should be passed Leticia', 'Then step is not correct, found "{}"'.format(
            third_step)

    @patch('click.echo', new_callable=Mock())
    def test_parse_file_with_tags(self, mock_print):
        feature_path = os.path.abspath(
            os.path.dirname(__file__) + '/../coverage/one_fail/features/getting_started.feature')
        self.features.parse_file(feature_path)
        assert len(
            self.features.scenarios) == 2, 'Expected to parse 2 scenarios from the feature file'

        name = self.features.scenarios[0].name
        tags = self.features.scenarios[0].tags
        steps = self.features.scenarios[0].steps
        first_step = '{} {}'.format(steps[0][0], steps[0][1])
        second_step = '{} {}'.format(steps[1][0], steps[1][1])
        third_step = '{} {}'.format(steps[2][0], steps[2][1])

        assert name == 'Getting started incorrect', 'The first scenario name is incorrect, found "{}"'.format(
            name)
        assert '|'.join(
            tags) == '@tag|@long-tag', 'First scenario tags are incorrect, found "{}"'.format('|'.join(tags))
        assert first_step == 'given I have given passed', 'Given step is not correct, found "{}"'.format(
            first_step)
        assert second_step == 'when I pass by when', 'Given step is not correct, found "{}"'.format(
            second_step)
        assert third_step == 'then should be passed Danilo', 'Given step is not correct, found "{}"'.format(
            third_step)

        name = self.features.scenarios[1].name
        tags = self.features.scenarios[1].tags
        steps = self.features.scenarios[1].steps
        first_step = '{} {}'.format(steps[0][0].lower(), steps[0][1])
        second_step = '{} {}'.format(steps[1][0].lower(), steps[1][1])
        third_step = '{} {}'.format(steps[2][0].lower(), steps[2][1])

        assert name == 'Getting started correct', 'The first scenario name is incorrect, found "{}"'.format(
            name)
        assert '|'.join(
            tags) == '@short-tag', 'First scenario tags are incorrect, found "{}"'.format('|'.join(tags))
        assert first_step == 'given I have given passed', 'Given step is not correct, found "{}"'.format(
            first_step)
        assert second_step == 'when I pass by when', 'When step is not correct, found "{}"'.format(
            second_step)
        assert third_step == 'then should be passed Leticia', 'Then step is not correct, found "{}"'.format(
            third_step)


if __name__ == '__main__':
    unittest.main()
