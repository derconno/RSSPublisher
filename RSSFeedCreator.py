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
import datetime
import hashlib

import PyRSS2Gen

import config


class Feed:
    def __init__(self, title, link, description, items=[]):
        self.title = title
        self.link = link
        self.description = description
        self.items = items

    def add_Item(self, title, link, description, author):
        item = PyRSS2Gen.RSSItem(title=title,
                                 link=link,
                                 description=description,
                                 author=author,
                                 guid=PyRSS2Gen.Guid(
                                     hashlib.sha1(
                                         (title +
                                          link +
                                          description +
                                          author +
                                          datetime.datetime.utcnow().strftime(
                                              "%Y-%m-%d %H:%M:%S")).encode()).hexdigest(),
                                     False),
                                 pubDate=datetime.datetime.utcnow())
        self.items.insert(0, item)
        self.items = self.items[:config.config['DEFAULT']['max_items']]
        config.config.save_items(self.items)

    def write(self, file):
        rss = PyRSS2Gen.RSS2(
            title=self.title,
            link=self.link,
            description=self.description,
            lastBuildDate=datetime.datetime.now(),
            items=self.items
        )
        rss.write_xml(open(file, "w"))
