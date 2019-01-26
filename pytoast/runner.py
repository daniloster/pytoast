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

    def run_step(self, step_stats, keyword, step_sentence):
        step_text = '{} {}'.format(keyword, step_sentence)
        step_stats['keyword'] = keyword
        step_stats['sentence'] = step_sentence
        step_stats['step'] = '%s %s' % (keyword, step_sentence)
        step_stats['status'] = True
        step_stats['start_time'] = time.time()

        (expression, step_lambda) = self.get_step(step_sentence)
        args = self.get_args(expression, step_sentence)
        try:
            step_lambda(**args)
        except AssertionError as error:
            step_stats['status'] = False
            step_stats['error'] = 'Assertion Error'
            step_stats['stack'] = traceback.format_exc()
        except:
            step_stats['status'] = False
            error = RuntimeError(sys.exc_info()[0])
            step_stats['error'] = error
            step_stats['stack'] = traceback.format_exc()
        finally:
            step_stats['end_time'] = time.time()
            step_stats['elapsed'] = step_stats['end_time'] - \
                step_stats['start_time']
            write = output.success if step_stats['status'] else output.error
            write(step_text)

            if self.config.verbose and not step_stats['status']:
                output.br()
                output.error(step_stats['stack'])
                output.br()

            return step_stats

    def run_scenario(self, scenario):
        scenario.stats['scenario'] = scenario.name
        scenario.stats['start_time'] = time.time()
        scenario.stats['elapsed'] = None
        scenario.stats['status'] = True
        scenario.stats['steps_stats'] = []
        try:
            rank = 0
            for (keyword, step_sentence) in scenario.steps:
                rank += 1
                scenario.stats['steps_stats'].append({
                    'rank': rank
                })
                step_stats = self.run_step(scenario.stats['steps_stats'][-1],
                                           keyword, step_sentence)
                step_stats['keyword'] = keyword
                status = scenario.stats['steps_stats'][-1]['status']
                if not status:
                    scenario.stats['status'] = False
        finally:
            scenario.stats['end_time'] = time.time()
            scenario.stats['elapsed'] = scenario.stats['end_time'] - \
                scenario.stats['start_time']
            return scenario.stats
