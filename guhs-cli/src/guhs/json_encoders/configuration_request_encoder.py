from guhs.guhs_configuration import GuhsConfiguration


def from_guhs_configuration(configuration: GuhsConfiguration):
    return {
        'targets': [
            {'order_id': t.order_id, 'name': t.name}
            for t in configuration.targets
        ],
        'boot_selection_timeout': configuration.boot_selection_timeout,
        'default_target': str(configuration.default_target.order_id)
    }