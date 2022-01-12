import json

import shell

STORAGE_FILE = '/opt/guhs/guhs_server.json'


def save(name, value):
    if not shell.file_exists(STORAGE_FILE):
        shell.write_file(STORAGE_FILE, json.dumps({name: value}))
        return

    configuration = json.loads(shell.read_file(STORAGE_FILE))
    configuration[name] = value

    shell.write_file(STORAGE_FILE, json.dumps(configuration))


def get(name):
    if not shell.file_exists(STORAGE_FILE):
        return None

    configuration = json.loads(shell.read_file(STORAGE_FILE))

    if name not in configuration:
        return None

    return configuration[name]
