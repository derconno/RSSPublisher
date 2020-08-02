##
## Copyright (c) 2019 Constantin Schwarz.
## 
## This file is part of RSSPublisher 
## (see https://github.com/derconno/RSSPublisher).
## 
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.
##
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from threading import Thread
from urllib import parse as urlparse

from FeedManager import FeedManager


def RSSRequestHandlerFactory():
    fm = FeedManager()

    class RSSRequestHandler(BaseHTTPRequestHandler):

        def do_GET(self):

            if self.path == '/feed.xml':
                # legacy compatiblity
                self.send_response(301)

                self.send_header('Location', '/feed?id=0')
                self.end_headers()

            elif self.path == '/post.html':

                self.send_response(200)

                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(open(path.join('sites', 'post.html'), 'rb').read())

            elif self.path.startswith("/feed?"):

                try:
                    args = dict(arg.split('=', 1) for arg in self.path[6:].split('&'))
                except ValueError:
                    self.respond_404()
                    return

                if not 'id' in args.keys():
                    self.respond_404()
                    return

                xml = fm.getFeed(args['id'])

                self.send_response(200)

                self.send_header('Content-type', 'application/xhtml+xml')
                self.end_headers()

                self.wfile.write(bytes(xml, 'utf-8'))
            else:
                self.respond_404()
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

                if 'id' in data.keys():
                    id = data['id']
                else:
                    id = 0

                if fm.isValidSecret(id, data['secret']):
                    self.send_response(200)

                    self.end_headers()
                    self.wfile.write(b'success\n')

                    fm.addItem(id,
                               title=data['title'],
                               link=data['link'],
                               description=data['description'],
                               author=data['author'])
                else:
                    self.send_response(403)

                    self.end_headers()
                    self.wfile.write(b'unauthorized\n')

            else:
                self.respond_404()
            return

        def respond_404(self):
            self.send_response(404)

            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(open(path.join('sites', '404.html'), 'rb').read())

    return RSSRequestHandler


class RSSServer(Thread):

    def __init__(self, addr, sock):
        Thread.__init__(self)
        self.addr = addr
        self.sock = sock
        self.daemon = True
        self.start()

    def run(self):
        handler = RSSRequestHandlerFactory()
        httpd = HTTPServer(self.addr, handler, False)
        httpd.socket = self.sock
        httpd.server_bind = self.server_close = lambda self: None

        httpd.serve_forever()
