import sys
from datetime import datetime
from enum import Enum
from threading import Lock

from clint.textui.colored import cyan, green, yellow, blue, magenta, red, white

from src.connection.tor.config import TorLogType, set_log_type
from src.etc import log_path

_colors = {
    'SYSTEM': cyan,
    'WARN': magenta,
    'ERROR': red,
    'PROGRESS_START': blue,
    'PROGRESS_ON_GOING': yellow,
    'PROGRESS_FINISH': green,
    'MESSAGE': white
}


class MessageType(Enum):
    SYSTEM = 'system'
    WARN = 'warn'
    ERROR = 'error'
    PROGRESS_START = 'start'
    PROGRESS_ON_GOING = 'progress'
    PROGRESS_FINISH = 'finish'
    MESSAGE = 'message'


class LogLevel(Enum):
    QUIET = 1
    HUSH = 2
    MINIMAL = 3
    NORMAL = 4
    FULL = 5
    DEBUG = 6
    ALL = 7


class MessageLevel(Enum):
    ERROR = 0
    WARN = 1
    SYSTEM = 2
    MINIMAL_INFO = 3
    NORMAL_INFO = 4
    FULL_INFO = 5
    DEBUG = 6
    MISC = 7


_write_locks = []

_global_log_level = LogLevel.NORMAL.value
_global_write_lock = Lock()


def set_global_log_level(log_level):
    global _global_log_level
    _global_log_level = log_level.value
    if log_level == LogLevel.DEBUG:
        set_log_type(TorLogType.MINIMAL)


def get_lock(stdout):
    global _write_locks
    for l in _write_locks:
        if l[0] == stdout:
            return l[1]
    lock = Lock()
    _write_locks.append((stdout, lock))
    return lock


class Logger:
    def __init__(self, log_level, stdout=sys.stdout):
        self._stdout = stdout
        self._log_level = log_level.value
        self._write_lock = get_lock(stdout)

    def log(self, message, message_type, message_level):
        if message_level.value <= self._log_level:
            self._write_lock.acquire()
            print(_format_log(message, message_type), file=self._stdout)
            self._stdout.flush()
            self._write_lock.release()
            log(message, message_type, message_level)


def log(message, message_type, message_level):
    global _global_log_level, _global_write_lock
    if message_level.value <= _global_log_level:
        _global_write_lock.acquire()
        print(_format_log(message, message_type))
        sys.stdout.flush()
        _global_write_lock.release()


def new_log_file(class_name):
    log_dir = log_path.joinpath('%s/' % class_name)
    if not log_dir.exists():
        log_dir.mkdir()
    log_name = '%s.log' % datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
    return open(log_dir.joinpath(log_name), 'w')


def _format_log(message, message_type):
    fmt = _colors[message_type.name]
    time = datetime.now().strftime('%H:%M.%S')
    return fmt('%s [%s]: %s' % (time, message_type.value, message))


if __name__ == '__main__':
    l1 = Logger(LogLevel.ALL)
    l2 = Logger(LogLevel.DEBUG, stdout=new_log_file('logger_v2.__main__'))

    l1.log('Test message', MessageType.MESSAGE, MessageLevel.MISC)
    l2.log('Test message', MessageType.MESSAGE, MessageLevel.MISC)
    l1.log('Test debug message', MessageType.WARN, MessageLevel.DEBUG)
    l2.log('Test debug message', MessageType.WARN, MessageLevel.DEBUG)
