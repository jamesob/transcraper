"""
Abstract base class for scrapers.
"""

import abc


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

    @property
    def id(self):
        """Provide a source identifier (str) for this scraper."""
        safe_username = self.username[:-3] + ('*' * 3)
        institution_name = self.__class__.__name__

        return "%s@%s" % (safe_username, institution_name)

