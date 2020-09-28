from datetime import datetime
from threading import Thread
from time import sleep, mktime

import feedparser

from core.FeedCreator import Feed
from core.FeedManager import FeedManager


class Updater(Thread):

    def __init__(self, fm: FeedManager, update_interval=900):
        Thread.__init__(self)
        self.feed_manager = fm
        self.update_interval = update_interval
        self.daemon = True
        self.start()

    def run(self) -> None:
        last_poll = {}
        while True:
            polling_feeds = self.feed_manager.get_polling_feeds()
            for id in polling_feeds.keys():
                if id not in last_poll.keys():
                    self.do_poll(polling_feeds[id])
                    last_poll[id] = datetime.utcnow()
                else:
                    if (datetime.utcnow() - last_poll[id]).total_seconds() > self.update_interval:
                        self.do_poll(polling_feeds[id])
                        last_poll[id] = datetime.utcnow()

            sleep(60)

    def do_poll(self, feed: Feed):
        print("[{}] Updating feed: {}".format(datetime.now(), feed.link))
        last_update = feed.get_latest_item_pubDate()
        polled = feedparser.parse(feed.link)
        for item in polled.entries:
            if datetime.fromtimestamp(mktime(item.published_parsed)) > last_update:
                title = link = description = author = ''
                try:
                    title = item.title
                except:
                    pass
                try:
                    link = item.link
                except:
                    pass
                try:
                    description = item.description
                except:
                    pass
                try:
                    author = item.author
                except:
                    pass

                feed.add_Item(
                    title=title,
                    link=link,
                    description=description,
                    author=author,
                    pubDate=datetime.fromtimestamp(mktime(item.published_parsed))
                )
        feed.saveItems()
