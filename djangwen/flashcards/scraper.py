import abc
from collections import Counter


class Scraper():

    def __init__(self, url=None):
        self.url = url
        self.title = None
        self.words = Counter()

    @abc.abstractmethod
    def process_page(self):
        returnh
