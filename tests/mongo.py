
from unittest import TestCase
from nose.tools import eq_
import datetime

from transcraper.storage import MongoTransactions
from transcraper import Transaction


class MongoTransactionsTest(TestCase):

    def setUp(self):
        self.now = datetime.datetime.utcnow()
        self.datastore = MongoTransactions(collection_name='mongo_test')
        self.trans = Transaction('testtrans', 12, self.now, 'unittest')

    def tearDown(self):
        self.datastore.dropDatabase()

    def test_add_dup(self):
        """Ensure we don't add a duplicate transaction."""
        for i in range(3):
            self.datastore.save(self.trans)

        eq_(1, self.datastore._collection.count())
