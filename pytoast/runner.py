import re
import time
import sys
from pytoast import output
import traceback


class Runner(object):

    def __init__(self, config):
        self.steps = []
        self.map = {}
        self.config = config

    def clear(self):
        self.steps = []
        self.map = {}

    def add_step_definition(self, expression, func):
        self.steps.append(expression)
        self.map[expression] = func

    def get_step(self, step_sentence):
        """

        """
        steps_candidates = [expression for expression in self.steps
                            if re.compile(expression, re.IGNORECASE)
                                 .search(step_sentence)]
        if len(steps_candidates) == 0:
            raise LookupError('No step found matching "{}"'.format(
                step_sentence))

        step_candidate = steps_candidates[0]
        step_function = self.map.get(step_candidate)
        return (step_candidate, step_function)

    def get_args(self, expression, step_sentence):
        regex = re.compile(expression, re.IGNORECASE)
        groups = regex.search(step_sentence).groupdict()
        return groups

    def run_step(self, steps_stats, keyword, step_sentence):
        step_text = '{} {}'.format(keyword, step_sentence)
        steps_stats[step_sentence] = {
            'status': True,
            'start_time': time.time()
        }
        (expression, step_lambda) = self.get_step(step_sentence)
        args = self.get_args(expression, step_sentence)
        try:
            step_lambda(**args)
        except AssertionError as error:
            steps_stats[step_sentence]['status'] = False
            steps_stats[step_sentence]['error'] = 'Assertion Error'
            steps_stats[step_sentence]['stack'] = traceback.format_exc()
        except:
            steps_stats[step_sentence]['status'] = False
            error = RuntimeError(sys.exc_info()[0])
            steps_stats[step_sentence]['error'] = error
            steps_stats[step_sentence]['stack'] = traceback.format_exc()
        finally:
            steps_stats[step_sentence]['end_time'] = time.time()
            steps_stats[step_sentence]['elapsed'] = steps_stats[step_sentence]['end_time'] - \
                steps_stats[step_sentence]['start_time']
            write = output.success if steps_stats[step_sentence]['status'] else output.error
            write('{} \t\t\t step stats (ellapsed: {}, success: {}) \
                  '.format(step_text,
                           steps_stats[step_sentence]['elapsed'],
                           steps_stats[step_sentence]['status']))
            if self.config.verbose and not steps_stats[step_sentence]['status']:
                output.br()
                output.error(steps_stats[step_sentence]['stack'])
                output.br()

            return steps_stats[step_sentence]

    def run_scenario(self, scenario):
        scenario.stats['start_time'] = time.time()
        scenario.stats['status'] = True
        scenario.stats['steps_stats'] = {}
        try:
            for (keyword, step_sentence) in scenario.steps:
                step_stats = self.run_step(scenario.stats['steps_stats'],
                                           keyword, step_sentence)
                step_stats['keyword'] = keyword
                status = scenario.stats['steps_stats'][step_sentence]['status']
                if not status:
                    scenario.stats['status'] = False
        finally:
            scenario.stats['end_time'] = time.time()
            return scenario.stats
