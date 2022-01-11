import unittest
from http import HTTPStatus

import pytest
from mock.mock import patch
from requests import Response

from guhs import guhs_configurator
from guhs.guhs_configuration import GuhsConfiguration, Target
from guhs.guhs_configurator import GUHS_GRUB_FILENAME, GuhsConfigurationError


class TestGuhsConfigurator(unittest.TestCase):
    def setUp(self):
        self.post = patch('requests.post').start()
        self.get = patch('requests.get').start()
        self.grub_boot_targets = patch('guhs.grub.grub_service.boot_targets').start()
        self.grub_deploy_script = patch('guhs.grub.grub_service.deploy_script').start()
        self.grub_read_script = patch('guhs.grub.grub_service.read_script').start()
        self.grub_scripts = patch('guhs.grub.grub_service.scripts').start()
        self.grub_remove_script = patch('guhs.grub.grub_service.remove_script').start()
        self.grub_default_target = patch('guhs.grub.grub_service.default_target').start()
        self.grub_boot_selection_timeout = patch('guhs.grub.grub_service.boot_selection_timeout').start()
        self.read_file = patch('guhs.shell.read_file').start()
        self.write_file = patch('guhs.shell.write_file').start()
        self.file_exists = patch('guhs.shell.file_exists').start()

    def tearDown(self):
        patch.stopall()

    def test_it_returns_current_configuration(self):
        self.grub_boot_targets.return_value = ['First', 'Second']
        self.grub_default_target.return_value = 1
        self.grub_boot_selection_timeout.return_value = 10
        self.grub_scripts.return_value = []

        configuration = guhs_configurator.current()

        assert configuration == GuhsConfiguration(
            False,
            targets=[Target(1, 'First'), Target(2, 'Second')],
            boot_selection_timeout=10,
            default_target=Target(2, 'Second')
        )
        self.grub_scripts.assert_called_once()

    def test_it_overrides_grub_configuration_with_guhs_http_server(self):
        response = response_ok()
        response.json = lambda: {
            'targets': [
                {'order_id': 1, 'name': 'First'},
                {'order_id': 2, 'name': 'Second'},
            ],
            'boot_selection_timeout': 5,
            'default_target': '1'
        }
        self.get.return_value = response
        self.grub_boot_targets.return_value = ['First', 'Second']
        self.grub_default_target.return_value = 1
        self.grub_boot_selection_timeout.return_value = 10
        self.grub_scripts.return_value = [GUHS_GRUB_FILENAME]
        self.grub_read_script.return_value = guhs_configurator.generate_grub_script('fqdn')

        configuration = guhs_configurator.current()

        assert configuration == GuhsConfiguration(
            True,
            targets=[Target(1, 'First'), Target(2, 'Second')],
            server='fqdn',
            default_target=Target(1, 'First'),
            boot_selection_timeout=5
        )
        self.get.assert_called_with('fqdn/api/configuration')
        self.grub_read_script.assert_called_once_with(GUHS_GRUB_FILENAME)

    def test_it_installs_server(self):
        self.post.return_value = response_ok()
        self.grub_boot_targets.return_value = ['name', 'name2']
        self.grub_boot_selection_timeout.return_value = 10
        self.grub_scripts.return_value = []

        guhs_configurator.install('fqdn')

        self.post.assert_called_once_with(
            'fqdn',
            json={
                'targets': [
                    {'order_id': 1, 'name': 'name'},
                    {'order_id': 2, 'name': 'name2'},
                ],
                'boot_selection_timeout': 10,
                'default_target': '2'
            }
        )
        self.grub_deploy_script(
            GUHS_GRUB_FILENAME,
            guhs_configurator.generate_grub_script('fqdn')
        )

    def test_set_parameter(self):
        self.post.return_value = response_ok()
        self.grub_scripts.return_value = [GUHS_GRUB_FILENAME]
        self.grub_read_script.return_value = guhs_configurator.generate_grub_script('fqdn')

        guhs_configurator.set('default-target', '1')

        self.post.assert_called_once_with(
            'fqdn/api/set',
            json={'parameter': 'default_target', 'value': '1'}
        )

    def test_it_fails_setting_parameter_without_installation(self):
        self.grub_scripts.return_value = []

        with pytest.raises(GuhsConfigurationError):
            guhs_configurator.set('default-target', '1')

    def test_it_fails_setting_non_existing_parameter(self):
        with pytest.raises(GuhsConfigurationError):
            guhs_configurator.set('a', '1')

    def test_get_parameter(self):
        response = response_ok()
        response.json = lambda: {'value': 5}
        self.get.return_value = response
        self.grub_read_script.return_value = guhs_configurator.generate_grub_script('fqdn')
        self.grub_scripts.return_value = [GUHS_GRUB_FILENAME]

        assert guhs_configurator.get('boot-selection-timeout') == 5

        self.get.assert_called_once_with('fqdn/api/get/boot_selection_timeout')

    def test_uninstall(self):
        self.grub_scripts.return_value = [GUHS_GRUB_FILENAME]

        guhs_configurator.uninstall()

        self.grub_remove_script.assert_called_once_with(GUHS_GRUB_FILENAME)

    def test_uninstall_without_installation(self):
        self.grub_scripts.return_value = []

        guhs_configurator.uninstall()

        self.grub_remove_script.assert_not_called()


def response_ok():
    response = Response()
    response.status_code = HTTPStatus.OK
    return response


def response_not_found():
    response = Response()
    response.status_code = HTTPStatus.NOT_FOUND
    return response
