from dataclasses import dataclass
from enum import Enum
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


class GuhsParameters(str, Enum):
    DEFAULT_TARGET = 'default-target'
    BOOT_SELECTION_TIMEOUT = 'boot-selection-timeout'

    @classmethod
    def list(cls):
        return list(map(lambda parameter: parameter.value, cls))

