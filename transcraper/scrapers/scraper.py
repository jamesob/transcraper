"""
Abstract base class for scrapers.
"""

import abc
from selenium import webdriver


class Scraper(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @abc.abstractmethod
    def get_transactions(self):
        """
        Method which delivers a list of recent Transactions to be persisted.

        Returns:
            [Transaction, ...]
        """
        pass

    def _clean_amount(self, amount):
        """Clean incoming amount strings."""
        return amount.replace('$', '').replace(',', '')

    @property
    def id(self):
        """Provide a source identifier (str) for this scraper."""
        safe_username = self.username[:-3] + ('*' * 3)
        institution_name = self.__class__.__name__

        return "%s@%s" % (safe_username, institution_name)


class SeleniumScraper(Scraper):

    homepage_url = None
    cookies = []

    def __init__(self, username, password):
        super(SeleniumScraper, self).__init__(username, password)
        self.driver = webdriver.Firefox()

        self.driver.get(self.homepage_url)

    def _goto_link(self, text):
        """Follow a link with a WebDriver."""
        l = self.driver.find_element_by_partial_link_text(text)
        self.driver.get(l.get_attribute('href'))

    def close(self):
        self.driver.quit()

