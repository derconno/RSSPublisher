from PyRSS2Gen import RSSItem


class BaseFilter:

    def accept(self, item: RSSItem):
        return True

    def modify(self, item: RSSItem):
        return item
