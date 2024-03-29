from enum import Enum
from src.etc import resources_path


class TorLogType(Enum):
    FULL = ''
    MINIMAL = '--hush'
    NONE = '--quiet'


_start_port = 50000
_log_type = TorLogType.NONE
_log_file = resources_path.joinpath('logs/')


def set_log_type(tor_log_type):
    global _log_type
    _log_type = tor_log_type


def log_type():
    return _log_type


def start_port():
    return _start_port
