def generate(target, timeout):
    return (
        f'set timeout={timeout}\n'
        f'set default={target}\n'
    )
