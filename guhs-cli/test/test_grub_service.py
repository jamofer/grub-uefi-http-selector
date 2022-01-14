import unittest

import pytest
from mock.mock import patch, call

from helpers import grub_cfg_sample
from helpers.default_grub_sample import generate_default_grub
from guhs.grub import grub_service
from guhs.grub.grub_service import GRUB_CFG_PATH, GRUB_CONFIG_FOLDER, GrubServiceError, GRUB_DEFAULT_PATH


class TestGrubService(unittest.TestCase):
    def setUp(self):
        self.read_file = patch('guhs.shell.read_file').start()
        self.write_file = patch('guhs.shell.write_file').start()
        self.remove_file = patch('guhs.shell.remove_file').start()
        self.files_in_path = patch('guhs.shell.files_in_path').start()
        self.execute_command = patch('guhs.shell.execute_command').start()

    def test_it_parses_boot_targets(self):
        self.read_file.return_value = grub_cfg_sample.GRUB_CFG

        targets = grub_service.boot_targets()

        assert targets == ['Ubuntu', 'Windows Boot Manager (on /dev/nvme0n1p1)', 'UEFI Firmware Settings']
        self.read_file.assert_called_once_with(GRUB_CFG_PATH)

    def test_it_deploys_script(self):
        self.execute_command.return_value = (0, "", "")

        grub_service.deploy_script('03_asd', 'asddfasd')

        self.write_file.assert_called_once_with(f'{GRUB_CONFIG_FOLDER}/03_asd', 'asddfasd')
        self.execute_command.assert_has_calls([
            call(f'chmod +x {GRUB_CONFIG_FOLDER}/03_asd'),
            call('/usr/sbin/update-grub')
        ])

    def test_it_fails_deploying_script(self):
        self.execute_command.return_value = (1, "", "")

        with pytest.raises(GrubServiceError):
            grub_service.deploy_script('03_asd', 'asddfasd')

        self.write_file.assert_called_once_with(f'{GRUB_CONFIG_FOLDER}/03_asd', 'asddfasd')
        self.execute_command.assert_has_calls([
            call(f'chmod +x {GRUB_CONFIG_FOLDER}/03_asd'),
            call('/usr/sbin/update-grub')
        ])
        self.remove_file.assert_called_once_with(f'{GRUB_CONFIG_FOLDER}/03_asd')

    def test_it_returns_default_target(self):
        self.read_file.return_value = generate_default_grub(target=0)

        assert grub_service.default_target() == '0'

        self.read_file.assert_called_once_with(GRUB_DEFAULT_PATH)

    def test_it_returns_boot_selection_timeout(self):
        self.read_file.return_value = generate_default_grub(timeout=0)

        assert grub_service.boot_selection_timeout() == 0

        self.read_file.assert_called_once_with(GRUB_DEFAULT_PATH)

    def test_it_returns_grub_scripts(self):
        self.files_in_path.return_value = ['README', '00_aaa', '11_bbb']
        assert grub_service.scripts() == ['00_aaa', '11_bbb']

        self.files_in_path.assert_called_once_with(GRUB_CONFIG_FOLDER)
