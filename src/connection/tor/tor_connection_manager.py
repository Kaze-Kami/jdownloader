from threading import Lock

from src.connection.tor.config import start_port, log_type
from src.connection.tor.tor_connection import TorConnection
from src.util.logging.logger import Logger, LogLevel, MessageType, MessageLevel, new_log_file
from src.util.singleton import Singleton


class TorConnectionManager(metaclass=Singleton):
    def __init__(self):
        self._used_ports = []
        self._connections = []
        self._active_connections = []
        self._port_request_lock = Lock()
        self._logger = Logger(LogLevel.DEBUG, new_log_file('TorConnectionManager'))

    def _empty_port(self):
        self._port_request_lock.acquire()
        port = start_port()
        while port in self._used_ports:
            port += 2
        self._port_request_lock.release()
        return port

    def _unused_connection(self):
        con = None
        for c in self._connections:
            if c not in self._active_connections:
                con = c
        if not con:
            socks_port = self._empty_port()
            self._used_ports.append(socks_port)
            self._logger.log('Opening tor at ports %d and %d' % (socks_port, socks_port + 1), MessageType.SYSTEM,
                             MessageLevel.DEBUG)
            con = TorConnection(socks_port=socks_port, connection_manager=self, tor_log_type=log_type())
            self._connections.append(con)
        self._active_connections.append(con)
        return con

    def new_connection(self):
        return self._unused_connection()

    def on_connection_closed(self, connection):
        self._logger.log('Closing tor at ports %d and %d' % (connection.socks_port, connection.control_port),
                         MessageType.SYSTEM,
                         MessageLevel.DEBUG)
        self._connections.remove(connection)
        self._used_ports.remove(connection.socks_port)

    def on_connection_released(self, con):
        self._active_connections.remove(con)

    def close_connections(self):
        self._logger.log('Closing tor connections', MessageType.SYSTEM, MessageLevel.SYSTEM)
        for con in self._connections:
            con.close()
