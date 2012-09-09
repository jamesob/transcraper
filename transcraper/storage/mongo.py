"""
Contain routines for persisting information to mongo.
"""

import pymongo

import logging
log = logging.getLogger(__name__)


class MongoTransactions(object):
    """Provides access to the collection of transactions."""

    def __init__(self,
                 host='localhost',
                 port=27017,
                 db_name='transcraper',
                 collection_name='transactions'):
        self._db_name = db_name
        self._collection_name = collection_name
        self._connection = pymongo.Connection(host, port)
        self._db = self._connection[db_name]
        self._collection = self._db[collection_name]

    def save(self, transactions):
        """For a Transaction (or list of), save those not already in the
        datastore."""
        if not hasattr(transactions, '__iter__'):
            transactions = [transactions]

        num_saved = 0

        for t in transactions:
            is_in_db = self._collection.find({'id': t.id}).count() > 0

            if not is_in_db:
                self._collection.save(t.as_dict)
                num_saved += 1
            else:
                log.info("Skipping transaction %s. Already in datastore." % t)

        return num_saved

    def dropDatabase(self):
        return self._connection.drop_database(self._db_name)

