import sys

import logger
from guhs import guhs_configurator
from guhs.guhs_configuration import Target, GuhsProperties
from guhs.guhs_configurator import GuhsConfigurationError


def configure():
    configuration = guhs_configurator.current()
    boot_targets = _format_boot_targets(configuration.targets)

    server = input('GUHS HTTP server hostname/ip? ')
    set(GuhsProperties.SERVER, server)

    logger.info('Available boot targets:')
    logger.info(boot_targets)
    target = input(f'Default target? [{configuration.default_target.order_id}] ')
    if target:
        set(GuhsProperties.DEFAULT_TARGET, target)

    timeout = input(f'Boot selection timeout? [{configuration.boot_selection_timeout}] ')
    if timeout:
        set(GuhsProperties.BOOT_SELECTION_TIMEOUT, timeout)

    guhs_configurator.commit()


def show():
    configuration = guhs_configurator.current()

    if configuration.server is None:
        logger.error('GUHS was not found in the system. Did you configure it with "guhs-cli configure"')
        sys.exit(1)

    show_contents = (
        f'GUHS status: ENABLED\n'
        f'GUHS HTTP server: {configuration.server}\n'
        f'Default target: {_format_boot_target(configuration.default_target)}\n'
        f'Boot selection timeout: {configuration.boot_selection_timeout}'
    )

    logger.info(show_contents)
    return show_contents


def ls():
    configuration = guhs_configurator.current()
    boot_targets = _format_boot_targets(configuration.targets)

    logger.info(boot_targets)
    return boot_targets


def _format_boot_targets(targets: list[Target]):
    return '\n'.join(f'{_format_boot_target(t)}' for t in targets)


def _format_boot_target(target: Target):
    return f'{target.order_id}. {target.name}'


def set(name: str, value: str):
    _set(name, value)
    guhs_configurator.commit()


def _set(name, value):
    try:
        guhs_configurator.set(name, value)
    except GuhsConfigurationError as error:
        logger.error(f'Failed to set {name}={value}: {error}')
        sys.exit(1)


def get(name: str):
    value = _get(name)
    logger.info(value)

    return value


def _get(name):
    try:
        value = guhs_configurator.get(name)
    except GuhsConfigurationError as error:
        logger.error(f'Failed to get {name}: {error}')
        sys.exit(1)
    return value
