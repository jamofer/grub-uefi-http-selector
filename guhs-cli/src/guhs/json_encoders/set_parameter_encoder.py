from guhs.guhs_configuration import GuhsParameters


encoders = {
    GuhsParameters.DEFAULT_TARGET: str,
    GuhsParameters.BOOT_SELECTION_TIMEOUT: int,
}


def encode(name, value):
    return {'parameter': _encode_name(name), 'value': encoders[name](value)}


def _encode_name(parameter: str):
    return parameter.replace('-', '_')
