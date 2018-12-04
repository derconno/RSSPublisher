from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib import parse as urlparse

import RSSFeedCreator
import config

fc = RSSFeedCreator.Feed(title=config.title, link=config.link, description=config.description, items=config.get_items())
fc.write(path.join('sites', 'feed.xml'))

class RSSServer_RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == '/feed.xml':

            self.send_response(200)

            self.send_header('Content-type', 'application/xhtml+xml')
            self.end_headers()

            self.wfile.write(open(path.join('sites', 'feed.xml'), 'rb').read())

        elif self.path == '/post.html':

            self.send_response(200)

            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(open(path.join('sites', 'post.html'), 'rb').read())

        else:
            self.send_response(404)

            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(open(path.join('sites', '404.html'), 'rb').read())
        return

    def do_POST(self):
        if self.path == '/appendToFeed':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')

            data = {}
            for s in body.split('&'):
                (k, v) = s.split('=')
                k = k.replace('+', ' ')
                v = v.replace('+', ' ')
                data[urlparse.unquote(k)] = urlparse.unquote(v)


            if data['secret'] == config.secret:
                self.send_response(200)

                self.end_headers()
                self.wfile.write(b'success\n')

                fc.add_Item(title=data['title'],
                            link=data['link'],
                            description=data['description'],
                            author=data['author'])

                fc.write(path.join('sites', 'feed.xml'))
            else:
                self.send_response(200)

                self.end_headers()
                self.wfile.write(b'error\n')

        else:
            self.send_response(404)

            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(open(path.join('sites', '404.html'), 'rb').read())
        return

class RSSServer():

    def __init__(self):
        self.running = False

    def start_server(self, ip=config.ip, port=config.port):
        if self.running == False:
            self.server_address = (ip, port)
            self.httpd = HTTPServer(self.server_address, RSSServer_RequestHandler)
            self.running = True
            self.httpd.serve_forever()
        return

    def stop_server(self):
        if self.running:
            self.running = False
            self.httpd.shutdown()
        return
