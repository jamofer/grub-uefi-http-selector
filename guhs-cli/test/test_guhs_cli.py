import unittest
import pytest
from mock.mock import patch, call

import guhs_cli
from guhs.guhs_configuration import Target, GuhsConfiguration, GuhsProperties
from guhs.guhs_configurator import GuhsConfigurationError


class TestGuhsCli(unittest.TestCase):
    def setUp(self):
        self.configurator_set = patch('guhs.guhs_configurator.set').start()
        self.configurator_commit = patch('guhs.guhs_configurator.commit').start()
        self.configurator_get = patch('guhs.guhs_configurator.get').start()
        self.configurator_current = patch('guhs.guhs_configurator.current').start()
        self.input = patch('builtins.input').start()
        self.configurator_uninstall = patch('guhs.guhs_configurator.uninstall').start()
        self.configurator_install = patch('guhs.guhs_configurator.install').start()

    def tearDown(self):
        patch.stopall()

    def test_set_configuration(self):
        guhs_cli.set('default-target', '2')
        self.configurator_set.assert_called_with('default-target', '2')
        self.configurator_commit.assert_called()

    def test_it_fails_setting_configuration(self):
        self.configurator_set.side_effect = GuhsConfigurationError('message')

        with pytest.raises(SystemExit):
            guhs_cli.set('default-target', '2')

        self.configurator_set.assert_called_with('default-target', '2')
        self.configurator_commit.assert_not_called()

    def test_get_configuration(self):
        self.configurator_get.return_value = '2'

        value = guhs_cli.get('default-target')

        assert value == '2'

    def test_it_fails_getting_non_existing_configuration(self):
        self.configurator_get.side_effect = GuhsConfigurationError('message')

        with pytest.raises(SystemExit):
            guhs_cli.get('non-existing-configuration')

    def test_it_shows_boot_targets(self):
        self.configurator_current.return_value = GuhsConfiguration(
            True,
            [Target(1, 'One'), Target(2, 'Two')]
        )

        boot_targets = guhs_cli.ls()

        assert boot_targets == (
            '1. One\n'
            '2. Two'
        )

    def test_it_shows_current_configuration(self):
        targets = [Target(1, 'One'), Target(2, 'Two')]
        self.configurator_current.return_value = GuhsConfiguration(
            True,
            targets,
            server='192.168.1.1',
            boot_selection_timeout=10,
            default_target=targets[0]
        )

        current = guhs_cli.show()

        assert current == (
            'GUHS status: ENABLED\n'
            'GUHS HTTP server: 192.168.1.1\n'
            'Default target: 1. One\n'
            'Boot selection timeout: 10'
        )

    def test_it_shows_is_not_enabled_when_guhs_not_installed(self):
        targets = [Target(1, 'One'), Target(2, 'Two')]
        self.configurator_current.return_value = GuhsConfiguration(False, targets)

        with pytest.raises(SystemExit):
            guhs_cli.show()

    def test_it_installs_guhs(self):
        self.input.side_effect = ["host", "target", "timeout"]

        guhs_cli.install()

        self.configurator_set.assert_has_calls([
            call(GuhsProperties.DEFAULT_TARGET, "target"),
            call(GuhsProperties.BOOT_SELECTION_TIMEOUT, "timeout"),
        ])
        self.configurator_commit.assert_called()

    def test_it_skips_configuring_target_when_is_empty(self):
        self.input.side_effect = ["host", "", "timeout"]

        guhs_cli.install()

        self.configurator_set.assert_called_once_with(
            GuhsProperties.BOOT_SELECTION_TIMEOUT, "timeout"
        )
        self.configurator_install.assert_called_once_with('host')
        self.configurator_commit.assert_called()

    def test_it_skips_configuring_timeout_when_is_empty(self):
        self.input.side_effect = ["host", "target", ""]

        guhs_cli.install()

        self.configurator_set.assert_called_once_with(
            GuhsProperties.DEFAULT_TARGET, "target"
        )
        self.configurator_install.assert_called_once_with('host')
        self.configurator_commit.assert_called()

    def test_it_stops_configuring_when_set_fails(self):
        self.input.side_effect = ["host", "target", "timeout"]
        self.configurator_set.side_effect = GuhsConfigurationError('message')

        with pytest.raises(SystemExit):
            guhs_cli.install()

        self.configurator_install.assert_called_once_with('host')
        self.configurator_commit.assert_not_called()

    def test_it_uninstalls(self):
        guhs_cli.uninstall()
        self.configurator_uninstall.assert_called_once()
