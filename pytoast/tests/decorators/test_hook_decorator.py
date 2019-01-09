import unittest
from pytoast.settings import config
from pytoast.decorators import hook


class TestHookDecorator(unittest.TestCase):

    def setUp(self):
        config.hooks = {
            'after_all': [],
            'after_each': [],
            'before_all': [],
            'before_each': []
        }
        config.fail_fast = False
        config.verbose = False

    def test_hook_before_all(self):
        count = 0

        @hook(event='before_all')
        def before_all_hook():
            nonlocal count
            count += 2

        @hook(event='before_all')
        def second_before_all_hook():
            nonlocal count
            count += 4

        assert len(config.hooks.get('before_all')
                   ) == 2, 'There should be 2 hooks added to before_all'

        config.before_all()
        assert count == 6, 'All hooks for before_all should be executed'

    def test_hook_before_each(self):
        count = 0

        @hook(event='before_each')
        def before_all_hook():
            nonlocal count
            count += 2

        @hook(event='before_each')
        def second_before_each_hook():
            nonlocal count
            count += 4

        assert len(config.hooks.get('before_each')
                   ) == 2, 'There should be 2 hooks added to before_each'

        config.before_each()
        assert count == 6, 'All hooks for before_each should be executed'

    def test_hook_after_each(self):
        count = 0

        @hook(event='after_each')
        def before_all_hook():
            nonlocal count
            count += 2

        @hook(event='after_each')
        def second_after_each_hook():
            nonlocal count
            count += 4

        assert len(config.hooks.get('after_each')
                   ) == 2, 'There should be 2 hooks added to after_each'

        config.after_each()
        assert count == 6, 'All hooks for after_each should be executed'

    def test_hook_after_all(self):
        count = 0

        @hook(event='after_all')
        def before_all_hook():
            nonlocal count
            count += 2

        @hook(event='after_all')
        def second_after_all_hook():
            nonlocal count
            count += 4

        assert len(config.hooks.get('after_all')
                   ) == 2, 'There should be 2 hooks added to after_all'

        config.after_all()
        assert count == 6, 'All hooks for after_all should be executed'

    def test_hook_unexpected(self):
        count = 0

        try:

            @hook(event='different')
            def before_all_hook():
                nonlocal count
                count += 2

            @hook(event='different')
            def second_after_all_hook():
                nonlocal count
                count += 4

        except RuntimeError as e:
            samples = ', '.join(
                ['"after_all"', '"after_each"', '"before_all"', '"before_each"'])
            message = 'A hook must have event as either {}'.format(samples)
            assert str(e) == message, 'Incorrect error raised'

        assert count == 0, 'hook decorator accepted hook event different from the expected ones'


if __name__ == '__main__':
    unittest.main()
