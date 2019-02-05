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
from urllib import parse as urlparse

import RSSFeedCreator
import config

fc = RSSFeedCreator.Feed(title=config.config['DEFAULT']['title'], link=config.config['DEFAULT']['link'],
                         description=config.config['DEFAULT']['description'], items=config.get_items())
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

            if data['secret'] == config.config['DEFAULT']['secret']:
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

    def start_server(self, ip=config.config['DEFAULT']['ip'], port=int(config.config['DEFAULT']['port'])):
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
