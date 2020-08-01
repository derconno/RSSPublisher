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
import os
import pickle

import PyRSS2Gen

class Feed:
    def __init__(self, title, link, description, itemsfile, items=None, maxitems=50):
        if items is None:
            items = []
        self.title = title
        self.link = link
        self.description = description
        self.items = items
        self.maxitems = maxitems
        self.itemsfile = itemsfile

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
        self.items = self.items[:self.maxitems]

    def getXml(self):
        rss = PyRSS2Gen.RSS2(
            title=self.title,
            link=self.link,
            description=self.description,
            lastBuildDate=datetime.datetime.now(),
            items=self.items
        )
        return rss.to_xml('utf-8')

    def saveItems(self):
        if not os.path.dirname(self.itemsfile) == '':
            os.makedirs(os.path.dirname(self.itemsfile), exist_ok=True)
        f = open(self.itemsfile, 'wb')
        pickle.dump(self.items, f)
        f.close()