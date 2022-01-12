import re
from http import HTTPStatus

from guhs import guhs_gateway
from guhs.grub import grub_service
from guhs.guhs_configuration import GuhsConfiguration, Target, GuhsParameters
from guhs.json_encoders import set_parameter_encoder, get_parameter_encoder, get_parameter_decoder
from guhs.json_encoders.configuration_request_encoder import from_guhs_configuration
from guhs.json_encoders.configuration_response_decoder import to_gush_configuration

GUHS_CONFIGURATION_FILENAME = 'boot_source.cfg'
GUHS_GRUB_FILENAME = '01_guhs'


def generate_grub_script(fqdn):
    return (
        '#! /bin/sh\n'
        'cat << EOF\n'
        'insmod net\n'
        'insmod efinet\n'
        'insmod http\n'
        '\n'
        'net_bootp\n'
        f'source (http,{fqdn})/{GUHS_CONFIGURATION_FILENAME}\n'
        'EOF\n'
    )


def current() -> GuhsConfiguration:
    configuration = _configuration_from_grub()

    if _is_installed():
        remote_configuration = _configuration_from_server()
        remote_configuration.targets = configuration.targets

        if remote_configuration.default_target not in configuration.targets:
            remote_configuration.default_target = configuration.default_target

        return remote_configuration

    return configuration


def _configuration_from_grub():
    grub_targets = grub_service.boot_targets()
    targets = []

    for i in range(len(grub_targets)):
        targets.append(Target(i+1, grub_targets[i]))

    grub_target = grub_service.default_target()
    default_target = targets[0]

    if re.match(r'\d+$', grub_target) is not None:
        default_target = targets[int(grub_target)]
    else:
        for target in targets:
            if grub_target == target:
                default_target = target

    return GuhsConfiguration(
        False,
        targets,
        boot_selection_timeout=grub_service.boot_selection_timeout(),
        default_target=default_target
    )


def _configuration_from_server():
    server = _configured_server_fqdn()
    response = guhs_gateway.get(server, '/api/configuration')
    remote_configuration = to_gush_configuration(response.json())
    remote_configuration.server = server

    return remote_configuration


def _configured_server_fqdn():
    gush_grub_script = grub_service.read_script(GUHS_GRUB_FILENAME)
    server = re.findall(r'\(http,(.*)\)', gush_grub_script)[0]
    return server


def install(fqdn):
    configuration = current()

    guhs_gateway.post(fqdn, '/api/configuration', from_guhs_configuration(configuration))
    grub_service.deploy_script(GUHS_GRUB_FILENAME, generate_grub_script(fqdn))


def set(name, value):
    if not _is_installed():
        raise GuhsConfigurationError('Install GUHS first.')
    if name not in GuhsParameters.list():
        raise GuhsConfigurationError(f'Unable to set {name}: parameter not found.')

    request_body = set_parameter_encoder.encode(name, value)

    response = guhs_gateway.post(_configured_server_fqdn(), '/api/set', request_body)

    if response.status_code != HTTPStatus.OK:
        raise GuhsConfigurationError(f'Unable to set {name} with {value} in remote server.')


def get(name):
    if not _is_installed():
        raise GuhsConfigurationError('Install GUHS first.')
    if name not in GuhsParameters.list():
        raise GuhsConfigurationError(f'Unable to set {name}: parameter not found.')

    encoded_name = get_parameter_encoder.encode_name(name)
    response = guhs_gateway.get(_configured_server_fqdn(), f'/api/get/{encoded_name}')

    return get_parameter_decoder.decode(response.json())


def uninstall():
    if _is_installed():
        grub_service.remove_script(GUHS_GRUB_FILENAME)


def _is_installed():
    return GUHS_GRUB_FILENAME in grub_service.scripts()


class GuhsConfigurationError(RuntimeError):
    pass
