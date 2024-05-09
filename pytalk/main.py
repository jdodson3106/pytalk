from http.server import HTTPServer, BaseHTTPRequestHandler


class PytalkHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        match self.path:
            case "/":
                print("in base path")
                return
            case "/echo":
                print("in echo")
                self.echoHandler()
                return
            case _:
                self.send_error(404, message='nah bitch...')
                return

    def echoHandler(self):
        content_length = int(self.headers.get("Content-Length"))
        body = self.rfile.read(content_length-1)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)


def run(server_class=HTTPServer, handler_class=PytalkHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def main():
    run()


if __name__ == "__main__":
    main()
