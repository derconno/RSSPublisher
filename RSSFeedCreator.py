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
        config.save_items(self.items)

    def write(self, file):
        rss = PyRSS2Gen.RSS2(
            title=self.title,
            link=self.link,
            description=self.description,
            lastBuildDate=datetime.datetime.now(),
            items=self.items
        )
        rss.write_xml(open(file, "w"))
