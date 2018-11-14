from http.server import BaseHTTPRequestHandler, HTTPServer


class RSSServer_RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        self.send_header('Content-type', 'application/xhtml+xml')
        self.end_headers()

        self.wfile.write(open('feed.xml', 'rb').read())
        return


class RSSServer():

    def __init__(self):
        self.running = False

    def start_server(self, port=8080):
        if self.running == False:
            self.server_address = ('127.0.0.1', port)
            self.httpd = HTTPServer(self.server_address, RSSServer_RequestHandler)
            self.running = True
            self.httpd.serve_forever()
        return

    def stop_server(self):
        if self.running:
            self.running = False
        return
