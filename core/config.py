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
import configparser

config = None


def default_config(path):
    global config
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'ip': '127.0.0.1',
        'port': '8000',
        'threads': '10',
        'feeds': 'feeds.ini',
        'polling interval': '900'
    }
    with open(path, 'w') as cfgfile:
        config.write(cfgfile)


def read_config(path):
    global config
    config = configparser.ConfigParser()
    config.read(path)
