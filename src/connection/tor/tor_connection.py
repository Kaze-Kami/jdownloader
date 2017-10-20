import subprocess
import sys
import time

import requests
from psutil import Process
from stem import Signal
from stem.control import Controller

from src import etc
from src.connection.tor.config import TorLogType
from src.util.logging.logger import Logger, MessageType, MessageLevel, LogLevel, new_log_file


class TorConnection:
    def __init__(self, socks_port, connection_manager, tor_log_type=TorLogType.NONE):
        self._logger = Logger(LogLevel.DEBUG, stdout=new_log_file('TorConnection'))
        self._connection_manager = connection_manager
        self._socks_port = socks_port
        self._control_port = socks_port + 1
        self._id = 'Tor@%d' % socks_port
        self._proxies = {
            'http': 'socks5://localhost:%d' % self.socks_port,
            'https': 'socks5://localhost:%d' % self.socks_port
        }
        self._in_use = False

        # start tor daemon
        self._logger.log('Starting %s' % self._id, MessageType.SYSTEM, MessageLevel.DEBUG)
        config_file_path = _generate_torrc_file(socks_port=self.socks_port, control_port=self.control_port)
        self._daemon = subprocess.Popen('"%s" %s -f "%s"' % (etc.tor_path, tor_log_type.value, config_file_path), shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        pass

    def change_ip(self):
        self._logger.log('Changing ip for %s' % self._id, MessageType.SYSTEM, MessageLevel.MISC)
        while True:
            try:
                with Controller.from_port(port=self.control_port) as c:
                    c.authenticate(etc.tor_password)
                    if c.is_newnym_available():
                        c.signal(Signal.NEWNYM)
                    else:
                        self._logger.log('No new ip available, keeping old', MessageType.WARN, MessageLevel.DEBUG)
                    return
            except Exception as e:
                self._logger.log('Error changing ip for %s, retrying. Ex: %s' % (self._id, e), MessageType.WARN, MessageLevel.WARN)
                time.sleep(1.5)

    def get(self, url, stream=False):
        while True:
            try:
                return requests.get(url, proxies=self.proxies, stream=stream)
            except Exception as e:
                self._logger.log('Bad connection for %s, changing ip. Ex: %s' % (self._id, e), MessageType.WARN,
                                 MessageLevel.DEBUG)
                self.change_ip()

    def acquire(self):
        if self._in_use:
            raise Exception('Attempt to acquire %s but already in use')
        self._in_use = True
        self.change_ip()

    def release(self):
        self._in_use = False
        self._connection_manager.on_connection_released(self)

    def close(self):
        # self._daemon.kill()
        self._kill_daemon()
        self._connection_manager.on_connection_closed(self)
        self._logger.log('Closed %s' % self._id, MessageType.SYSTEM, MessageLevel.DEBUG)

    def _kill_daemon(self):
        process = Process(self._daemon.pid)
        for p in process.children(recursive=True):
            p.kill()
        process.kill()

    @property
    def socks_port(self):
        return self._socks_port

    @property
    def control_port(self):
        return self._control_port

    @property
    def proxies(self):
        return self._proxies


def _generate_torrc_file(socks_port, control_port):
    path = etc.tor_data_dir.joinpath('torrc.%d' % socks_port)
    with open(path, 'w') as f:
        f.write('SocksPort %d\n' % socks_port)
        f.write('ControlPort %d\n' % control_port)
        f.write('DataDirectory %s\n' % etc.tor_data_dir.joinpath('tor.%d' % socks_port))
        f.write('HashedControlPassword %s' % etc.tor_password_hashed)
    return path
