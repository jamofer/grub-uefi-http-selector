from guhs.guhs_configuration import GuhsConfiguration


def set(name, value):
    pass


def commit():
    pass


def get(name):
    pass


def current() -> GuhsConfiguration:
    pass


def install(fqdn):
    pass


def uninstall():
    return None


class GuhsConfigurationError(RuntimeError):
    pass