import os.path


def read_file(path):
    with open(path) as file:
        return file.read()


def write_file(path, contents):
    with open(path, 'w') as file:
        return file.write(contents)


def file_exists(path):
    return os.path.isfile(path)
