
from unittest import TestCase
from nose.tools import eq_

from transcraper.scrapers.chase_amazon import ChaseAmazon


class ChaseScraperTest(TestCase):

    def setUp(self):
        self.s = ChaseAmazon('fake', 'pwd')

    def test_row_conversion(self):
        rows = [[u'09/03/2012', u'', u'Pending', u'TWC*TIME WARNER NYC', u'',
                 u'$75.34'],
                [u'09/03/2012', u'', u'Pending', u'BAR MATCHLESS', u'',
                 u'$21.00'],
                [u'09/03/2012', u'', u'Payment', u'Thanks', u'',
                 u'-$21.00'],
                [u'09/02/2012', u'', u'Pending', u'TACOMBI NYC', u'',
                 u'$42.50'],
                [u'09/02/2012',
                 u'09/03/2012',
                 u'Sale',
                 u'UNIQLO SOHO US0030',
                 u'',
                 u'$21.60'],
                [u'09/01/2012', u'09/02/2012', u'Sale', u'NETFLIX.COM', u'',
                 u'$7.99'],
                [u'09/01/2012',
                 u'09/03/2012',
                 u'Sale',
                 u'BIG GAY ICE CREAM SHOP',
                 u'',
                 u'$4.50']]

        trans = self.s._raw_rows_to_transactions(rows)

        eq_(len(rows), len(trans))

