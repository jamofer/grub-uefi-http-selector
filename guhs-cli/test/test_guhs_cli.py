import unittest
import pytest
from mock.mock import patch

import guhs_cli
from guhs.guhs_configuration import Target, GuhsConfiguration
from guhs.guhs_configurator import GuhsConfigurationError


class TestGuhsCli(unittest.TestCase):
    def setUp(self):
        self.configurator_set = patch('guhs.guhs_configurator.set').start()
        self.configurator_commit = patch('guhs.guhs_configurator.commit').start()
        self.configurator_get = patch('guhs.guhs_configurator.get').start()
        self.configurator_current = patch('guhs.guhs_configurator.current').start()

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
        self.configurator_current.return_value = GuhsConfiguration([Target(1, 'One'), Target(2, 'Two')])

        boot_targets = guhs_cli.ls()

        assert boot_targets == (
            '1. One\n'
            '2. Two'
        )

    def test_it_shows_current_configuration(self):
        targets = [Target(1, 'One'), Target(2, 'Two')]
        self.configurator_current.return_value = GuhsConfiguration(
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

    def test_it_shows_is_not_enabled_when_guhs_not_configured(self):
        targets = [Target(1, 'One'), Target(2, 'Two')]
        self.configurator_current.return_value = GuhsConfiguration(targets)

        with pytest.raises(SystemExit):
            guhs_cli.show()
