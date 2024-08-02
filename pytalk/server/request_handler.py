from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from pytalk.request.request import Request
from pytalk.logger.logger import get_logger
import os

logger = get_logger()


class PytalkRequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        logger.info("%s - %s" % (self.address_string(), format % args))

    def do_GET(self):

        request = Request(
            method=self.command,
            path=self.path,
            headers=self.headers
        )
        return request

    def do_POST(self):
        
        # Parse body into key-value pairs
        # Currently only accepts form data, html
        content_length = int(self.headers.get("Content-Length"))
        body = self.rfile.read(content_length).decode("utf-8")
        
        request = Request(
            method=self.command,
            path=self.path,
            body=body,
            headers=self.headers
        )

        # So I can send an error back to the sender
        # self.send_error(HTTPStatus.BAD_REQUEST, message="foobar")
        
        # But I can't send a valid response? Trying to echo request
        """Serve a GET request."""
        
        with open("./pytalk/server/dummy.html", "rb") as fin:
            fs = os.fstat(fin.fileno())
            logger.info(fs)
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(fs.st_size))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()

            to_write = fin.read()
            self.wfile.write(to_write)
