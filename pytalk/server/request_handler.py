from http.server import BaseHTTPRequestHandler
from request.request import Request

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
        # Currently only accepts form data
        content_length = int(self.headers.get("Content-Length"))
        body = self.rfile.read(content_length).decode("utf-8")
        body_lines = body.split("\r\n")
        
        form_data = {}
        for i, body_line in enumerate(body_lines): 
            if not body_line:
                continue
            if "name=" in body_line:
                key = body_line.split("name=")[-1][1:-1] #strip quotes
                value = body_lines[i+2]
                form_data[key] = value
        
        request = Request(
            method = self.command, 
            path = self.path,
            form_data = form_data,
            headers = self.headers
        )
        print(request.headers)
        return request
