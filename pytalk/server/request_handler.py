from http.server import BaseHTTPRequestHandler
from request.request import Request
from pytalk.logger.logger import get_logger

logger = get_logger()

class PytalkRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        request = Request(
            method = self.command, 
            path = self.path,
            headers = self.headers
        )
        return request 

    def do_POST(self):
        
        # Parse body into key-value pairs
        # Currently only accepts form data, html
        content_length = int(self.headers.get("Content-Length"))
        content_type = self.headers.get("Content-Type")
        body = self.rfile.read(content_length).decode("utf-8")
        
        request = Request(
            method = self.command, 
            path = self.path,
            body = body,
            headers = self.headers
        )
        logger.info(request)
        return request
