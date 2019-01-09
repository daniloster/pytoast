from pytoast.settings import config

allowed_hooks = ['after_all', 'after_each', 'before_all', 'before_each']


def hook(event=None):
    if not event or event.lower() not in allowed_hooks:
        samples = ', '.join([
            '"{}"'.format(allowed) for allowed in allowed_hooks
        ])
        message = 'A hook must have event as either {}'.format(samples)
        raise RuntimeError(message)

    def decorator(f):
        config.hooks[event].append(f)

    return decorator
