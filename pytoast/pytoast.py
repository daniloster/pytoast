import click
import sys
import os
import glob
from pytoast import output
from pytoast.settings import config, features
from pytoast.decorators import collect_steps
from pytoast.runner import Runner

runner = Runner(config)


def spin(tags, features_path, root_path, fail_fast, verbose):
    output.write('== Setting up Pytoast ==\n\nRoot: {}\nFeatures: {}\
                 \nFail fast: {}\nVerbose: {}'.format(root_path, features_path, fail_fast, verbose))
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
    config.before_all()
    has_failed = False
    for scenario in features.scenarios:
        if should_run_all or has_at_least_one_tag(scenario.tags):
            output.br()
            config.before_each()
            output.reset_indent()
            output.br()
            output.write('{}: {}'.format(output.c('Scenario', 'white'),
                                         output.c(scenario.name, 'cyan')))
            output.inc_indent()
            stats = runner.run_scenario(scenario)
            if not has_failed and not stats['status']:
                has_failed = True

            if fail_fast and has_failed:
                sys.exit(1)

            output.br()
            config.after_each()

    output.br()
    config.after_all()
    sys.exit(1 if has_failed else 0)


@click.command()
@click.option('--tags', default='', help='Tags to run, it will filter the scenarios that will get executed')
@click.option('--features', default='', help='Folder path to your "*.feature" files')
@click.option('--root', default='', help='The root folder path to your project')
@click.option('--fail-fast', is_flag=True, help='Define whether the process should abort when a scenario fail')
@click.option('--verbose', is_flag=True, help='Define whether display stacktrace for errors')
def run(tags, features, root, fail_fast, verbose):
    spin(tags, features, root, fail_fast, verbose)
