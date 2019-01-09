from pytoast import output


class Config(object):

    def __init__(self):
        self.hooks = {
            'after_all': [],
            'after_each': [],
            'before_all': [],
            'before_each': []
        }
        self.fail_fast = False
        self.verbose = False

    def before_all(self):
        output.reset_indent()
        output.write(output.c(':: before all', 'cyan'))
        [f() for f in self.hooks['before_all']]
        return

    def before_each(self):
        output.reset_indent()
        output.write(output.c(':: before each', 'cyan'))
        [f() for f in self.hooks['before_each']]
        return

    def after_all(self):
        output.reset_indent()
        output.write(output.c(':: after all', 'cyan'))
        [f() for f in self.hooks['after_all']]
        return

    def after_each(self):
        output.reset_indent()
        output.write(output.c(':: after each', 'cyan'))
        [f() for f in self.hooks['after_each']]
        return
