from guhs.guhs_configuration import GuhsConfiguration, Target


def to_gush_configuration(response_json):
    targets = [decode_target(target) for target in response_json['targets']]
    default_target = [
        t for t in targets
        if str(t.order_id) == response_json['default_target'] or t.name == response_json['default_target']
    ][0]

    return GuhsConfiguration(
        True,
        targets,
        boot_selection_timeout=response_json['boot_selection_timeout'],
        default_target=default_target,
    )


def decode_target(target):
    return Target(target['order_id'], target['name'])