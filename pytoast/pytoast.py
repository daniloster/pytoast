import click
import sys
import os
import glob
import traceback
from tabulate import tabulate
from pytoast import output
from pytoast.settings import config, features
from pytoast.decorators import collect_steps
from pytoast.runner import Runner

runner = Runner(config)


def run_context(task, failure_task, skip_exit=False):
    try:
        task()
        return True
    except:
        output.error(traceback.format_exc())
        failure_task()
        if not skip_exit:
            sys.exit(1)
        else:
            return False


def get_title(root_path, features_path, fail_fast, show_stats, verbose):
    return '== Setting up Pytoast ==\n\nRoot: {}\nFeatures: {}\
            \nFail fast: {}\nShow stats: {}\nVerbose: {}\
            '.format(root_path, features_path, fail_fast, show_stats, verbose)


def get_step_stats_row(step_stats):
    get_status_color = output.get_success if step_stats.get(
        'status') else output.get_error
    status = 'SUCCESS' if step_stats.get('status') else 'ERROR'

    return [
        '%s%s' % (output.get_indent(), output.get_warn(
            step_stats.get('rank'))),
        get_status_color(step_stats.get('keyword')),
        get_status_color(status),
        get_status_color(step_stats.get('elapsed'))
    ]


def print_stats(stats):
    output.br()
    scenario = output.get_success(stats.get('scenario')) if stats.get(
        'status') else output.get_error(stats.get('scenario'))
    output.write('Scenario: "%s" total_time: %s' % 
                 (scenario, stats['elapsed']))
    output.br()

    table_rows = [get_step_stats_row(step_stats)
                  for step_stats in stats.get('steps_stats')]
    table = tabulate(table_rows, headers=[
             '%s#' % output.get_indent(), 'Step', 'Status', 'Elapsed time'])

    output.write_raw(table)

    output.br()


def spin(tags, features_path, root_path, fail_fast, show_stats, verbose):
    output.write(get_title(root_path, features_path,
                           fail_fast, show_stats, verbose))
    if not os.path.isabs(features_path):
        features_path = os.path.realpath(features_path)
    # Appending features to the sys.path
    sys.path.append(features_path)
    if not os.path.isabs(root_path):
        root_path = os.path.realpath(root_path)
    # Appending steps to the sys.path
    sys.path.append(root_path)

    all_tags = [] if tags == '' else tags.split(' ')

    output.br()
    config.fail_fast = fail_fast
    config.verbose = verbose
    collect_steps(runner)

    feature_files = glob.glob('{}/*.feature'.format(features_path))
    output.br()
    for feature_file in feature_files:
        output.write('* collecting feature: {}'.format(feature_file))
        features.parse_file(feature_file)

    should_run_all = len(all_tags) == 0

    def has_at_least_one_tag(scenario_tags):
        total_found_tags = len(
            [tag for tag in all_tags if tag in scenario_tags])
        return total_found_tags > 0

    output.br()
    output.write('* running scenarios')
    output.br()
    run_context(config.before_all, config.after_all)

    has_failed = False
    for scenario in features.scenarios:
        if should_run_all or has_at_least_one_tag(scenario.tags):
            output.br()
            if run_context(config.before_each, config.after_each, skip_exit=True):
                output.reset_indent()
                output.br()
                output.write('{}: {}'.format(output.c('Scenario', 'white'),
                                             output.c(scenario.name, 'cyan')))
                output.inc_indent()
                stats = runner.run_scenario(scenario)
                if not has_failed and not stats['status']:
                    has_failed = True

                if show_stats:
                    output.br()
                    print_stats(stats)

                output.br()
                run_context(config.after_each,
                            lambda: output.warn(
                                'after_each failed, exit will be skipped'),
                            skip_exit=True)

                if fail_fast and has_failed:
                    # If scenario failed and it is fast fail
                    # we only want to leave the loop
                    break

    output.br()
    config.after_all()
    sys.exit(1 if has_failed else 0)


@click.command()
@click.option('--tags', default='', help='Tags to run, it will filter the scenarios that will get executed')
@click.option('--features', default='', help='Folder path to your "*.feature" files')
@click.option('--root', default='', help='The root folder path to your project')
@click.option('--fail-fast', is_flag=True, help='Define whether the process should abort when a scenario fail')
@click.option('--show-stats', is_flag=True, help='Define whether it displays time elapsed and status as separate block')
@click.option('--verbose', is_flag=True, help='Define whether display stacktrace for errors')
def run(tags, features, root, fail_fast, show_stats, verbose):
    spin(tags, features, root, fail_fast, show_stats, verbose)
