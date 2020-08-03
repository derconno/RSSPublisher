##
## Copyright (c) 2020 Constantin Schwarz.
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
import pickle
from configparser import ConfigParser

from core import config
import os
import importlib
import ast
from core.FeedCreator import Feed


class FeedManager:
    def __init__(self):
        self.secrets = {}
        self.feeds = {}
        self.feedConfig = ConfigParser()
        if os.path.isfile(config.config['DEFAULT']['feeds']):
            self.feedConfig.read(config.config['DEFAULT']['feeds'], 'utf-8')
        self.readFeeds()

    def readFeeds(self):
        for section in self.feedConfig.sections():
            id = self.feedConfig[section].get('id')
            title = self.feedConfig[section].get('title')
            link = self.feedConfig[section].get('link')
            description = self.feedConfig[section].get('description')
            max_items = self.feedConfig[section].getint('max_items')
            itemsfile = self.feedConfig[section].get('items file')
            filter_classes = ast.literal_eval(self.feedConfig[section].get('filters', '[]'))
            filters = []
            try:
                f = open(itemsfile, 'rb')
                items = pickle.load(f)
                f.close()
            except:
                items = []

            for filterclass in filter_classes:
                splits = filterclass.split('.')
                module = importlib.import_module("filters.{}".format(splits[0]))
                fclass = getattr(module, splits[1])
                filters.append(fclass())

            feed = Feed(title, link, description, itemsfile, items=items, maxitems=max_items, filters=filters)
            self.feeds[id] = feed

            self.secrets[id] = self.feedConfig[section].get('secret')

        if '0' not in self.feeds.keys():
            self.feeds['0'] = Feed(
                title='Fallback feed',
                link='',
                description='RSSPublisher uses this feed as a fallback when no other valid feed is specified',
                itemsfile='/dev/null',
                maxitems=0
            )

    def getFeed(self, id):
        if id in self.feeds.keys():
            return self.feeds[id].getXml()
        else:
            return self.feeds['0'].getXml()

    def addItem(self, id, title, link, description, author):
        if id in self.feeds.keys():
            feed = self.feeds[id]
        else:
            feed = self.feeds['0']

        feed.add_Item(title, link, description, author)
        feed.saveItems()

    def isValidSecret(self, id, secret):
        if id in self.secrets.keys():
            return secret == self.secrets[id]
        else:
            return False
