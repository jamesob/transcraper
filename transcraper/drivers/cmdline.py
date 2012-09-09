import getpass
from transcraper.scrapers import ChaseAmazon
from transcraper.storage import MongoTransactions

import logging
log = logging.getLogger(__name__)


def from_cmdline(ScraperClass=ChaseAmazon,
                 DatastoreClass=MongoTransactions):
    uname = raw_input("Username: ")
    passwd = getpass.getpass("password: ")

    sc = ScraperClass(uname, passwd)
    store = DatastoreClass()

    transactions = sc.get_transactions(uname, passwd)
    num_saved = store.save(transactions)

    print "Saved %d new transactions." % num_saved


if __name__ == '__main__':
    from_cmdline()
