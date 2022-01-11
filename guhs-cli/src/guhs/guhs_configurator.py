import re
from http import HTTPStatus

import requests

from guhs import shell
from guhs.grub import grub_service
from guhs.grub.grub_service import GRUB_CONFIG_FOLDER
from guhs.guhs_configuration import GuhsConfiguration, Target, GuhsParameters
from guhs.json_encoders import set_parameter_encoder, get_parameter_encoder, get_parameter_decoder
from guhs.json_encoders.configuration_request_encoder import from_guhs_configuration
from guhs.json_encoders.configuration_response_decoder import to_gush_configuration

GUHS_CONFIGURATION_FILENAME = 'boot_source'
GUHS_GRUB_FILENAME = '05_guhs'
GUHS_GRUB_PATH = f'{GRUB_CONFIG_FOLDER}/{GUHS_GRUB_FILENAME}'


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

    if shell.file_exists(GUHS_GRUB_PATH):
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

    return GuhsConfiguration(
        False,
        targets,
        boot_selection_timeout=grub_service.boot_selection_timeout(),
        default_target=targets[grub_service.default_target()]
    )


def _configuration_from_server():
    server = _configured_server_fqdn()
    response = requests.get(f'{server}/api/configuration')
    remote_configuration = to_gush_configuration(response.json())
    remote_configuration.server = server

    return remote_configuration


def _configured_server_fqdn():
    gush_grub_script = shell.read_file(GUHS_GRUB_PATH)
    server = re.findall(r'\(http,(.*)\)', gush_grub_script)[0]
    return server


def install(fqdn):
    configuration = current()

    requests.post(fqdn, json=from_guhs_configuration(configuration))
    grub_service.deploy_script(GUHS_GRUB_FILENAME, generate_grub_script(fqdn))


def set(name, value):
    if name not in GuhsParameters.list():
        raise GuhsConfigurationError(f'Unable to set {name}: parameter not found.')

    request_body = set_parameter_encoder.encode(name, value)

    url = f'{_configured_server_fqdn()}/api/set'
    response = requests.post(url, json=request_body)

    if response.status_code != HTTPStatus.OK:
        raise GuhsConfigurationError(f'Unable to set {name} with {value} in remote server.')


def get(name):
    if name not in GuhsParameters.list():
        raise GuhsConfigurationError(f'Unable to set {name}: parameter not found.')

    encoded_name = get_parameter_encoder.encode_name(name)
    url = f'{_configured_server_fqdn()}/api/get/{encoded_name}'
    response = requests.get(url)

    return get_parameter_decoder.decode(response.json())


def uninstall():
    return None


class GuhsConfigurationError(RuntimeError):
    pass