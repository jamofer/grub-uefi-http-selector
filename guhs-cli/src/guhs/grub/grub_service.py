import re

from guhs import shell

GRUB_CFG_PATH = '/boot/grub/grub.cfg'
GRUB_CONFIG_FOLDER = '/etc/grub.d'
GRUB_BOOT_FOLDER = '/boot'
GRUB_DEFAULT_PATH = '/etc/default/grub'


def boot_targets():
    contents = shell.read_file(GRUB_CFG_PATH)
    return re.findall(r"^menuentry '(.*?)'", contents, re.MULTILINE)


def deploy_script(filename, contents):
    path = f'{GRUB_CONFIG_FOLDER}/{filename}'
    shell.write_file(path, contents)
    rc, stdout, stderr = shell.execute_command('/usr/sbin/update-grub')

    if rc != 0:
        shell.remove_file(path)
        raise GrubServiceError(f'Failed updating GRUB with deployed script "{filename}". Removed')


def default_target():
    contents = shell.read_file(GRUB_DEFAULT_PATH)
    matches = re.findall(r'GRUB_DEFAULT=(.*)$', contents, re.MULTILINE)

    return matches[0]


def boot_selection_timeout():
    contents = shell.read_file(GRUB_DEFAULT_PATH)
    matches = re.findall(r'GRUB_TIMEOUT=(.*)$', contents, re.MULTILINE)

    return int(matches[0])


def scripts():
    files = shell.files_in_path(GRUB_CONFIG_FOLDER)
    return [f for f in files if re.match(r'\d\d_.*', f) is not None]


def remove_script(filename):
    shell.remove_file(f'{GRUB_CONFIG_FOLDER}/{filename}')


def read_script(filename):
    shell.read_file(f'{GRUB_CONFIG_FOLDER}/{filename}')


class GrubServiceError(RuntimeError): pass