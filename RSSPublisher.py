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
import argparse
import os

import config

parser = argparse.ArgumentParser(
    description="""Publish events to a RSS feed.
    
    RSSPublisher  Copyright (C) 2019  Constantin Schwarz

    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions; see LICENSE for details.\n
""")

parser.add_argument('-c', '--config', default='config.ini', help='config file, defaults to config.ini')

args = vars(parser.parse_args())

if os.path.isfile(args['config']):
    config.read_config(args['config'])
else:
    os.makedirs(os.path.dirname(args['config']))
    config.default_config(args['config'])

import RSSServer

server = RSSServer.RSSServer()

try:
    print("""
    RSSPublisher  Copyright (C) 2019  Constantin Schwarz

    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions; see LICENSE for details.\n
    """)
    print('Server started on default port')
    server.start_server()
except KeyboardInterrupt:
    print('stopping server')
    server.stop_server()
