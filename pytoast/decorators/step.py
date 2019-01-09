from pytoast import output

steps = []


def step(expression=None):
    global steps
    if not expression:
        raise RuntimeError('A step must have a match expression')

    def decorator(f):
        steps.append((expression, f))

    return decorator


def collect_steps(runner):
    for (expression, f) in steps:
        output.write('* adding step definition: {} \
                     '.format(expression))
        runner.add_step_definition(expression, f)
