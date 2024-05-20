import socketserver
import sys

from server.request_handler import PytalkRequestHandler


class PytalkServer:

    def __init__(self, port: int = 0, address: str = ''):
        self.port = port
        self.address = address
        self.handler = PytalkRequestHandler
        self.server = socketserver.TCPServer(
                server_address=(address, port),
                RequestHandlerClass=self.handler,
                bind_and_activate=False)

    def start(self):
        self._pre_start()
        try:
            self.server.server_bind()
            self.server.server_activate()
        except Exception as e:
            self.server.server_close()
            print(f"error starting the server :: {e}")
            sys.exit(1)

        print(f"Pytalk Server running at {self.server.server_address[0]}:{self.server.server_address[1]}")
        self.server.serve_forever(0.1)

    def _pre_start(self):
        """
        Reserved to perform any pre-server creation
        setup/validation that needs to occurr
        """
        if self.port is None:
            self.port = 0  # let the os pick the port
