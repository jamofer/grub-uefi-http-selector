def generate(target, timeout):
    return (
        f'set default="{target}"\n'
        f'set timeout="{timeout}"\n'
    ).encode('ascii')
