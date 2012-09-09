
from unittest import TestCase
from nose.tools import eq_
import datetime

from transcraper import Transaction


class TransactionCreationTest(TestCase):

    def setUp(self):
        self.name = 'cdj-200s'
        self.now = datetime.datetime.utcnow()
        self.source = 'unittest'

    def test_creation(self):
        t = Transaction(self.name, 12, self.now, self.source)

        eq_(self.now, t.occurred_at)
        eq_('12.00', str(t.amount))
        eq_(self.name, t.name)
        eq_('unittest', t.source)

    def test_creation_with_amt_str(self):
        t2 = Transaction(self.name, u"12.01", self.now, self.source)

        eq_('12.01', str(t2.amount))

    def test_id(self):
        ts = []

        for i in range(2):
            ts.append(Transaction(self.name, u'12.00', self.now, self.source))

        (t1, t2) = ts
        eq_(t1.id, t2.id)

        t2.amount = u'12.11'
        eq_(False, t1.id == t2.id)

