import unittest

from guhs import guhs_configurator


class TestGuhsConfigurator(unittest.TestCase):
    def setUp(self):
        pass

    def test_it_installs_server(self):
        guhs_configurator.install('fqdn')

        self.requests.post(
            'fqdn',
            json={
                'targets': {
                    "1": "One",
                    "2": "Two"
                },
            }
        )