from dataclasses import dataclass
from typing import Optional


@dataclass
class Target(object):
    order_id: int
    name: str


@dataclass
class GuhsConfiguration(object):
    installed: bool
    targets: list[Target]
    server: Optional[str] = None
    boot_selection_timeout: Optional[int] = None
    default_target: Optional[Target] = None

    def to_dict(self):
        return {

        }


class GuhsProperties:
    DEFAULT_TARGET = 'default-target'
    BOOT_SELECTION_TIMEOUT = 'boot-selection-timeout'
