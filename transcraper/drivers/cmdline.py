import getpass
from transcraper.scrapers import ChaseScraper, AllyScraper
from transcraper.storage import MongoTransactions

import logging
log = logging.getLogger(__name__)


def from_cmdline(ScraperClass=ChaseScraper,
                 DatastoreClass=MongoTransactions):
    uname = raw_input("Username: ")
    passwd = getpass.getpass("password: ")
    transactions = []

    sc = ScraperClass(uname, passwd)
    store = DatastoreClass()

    try:
        transactions = sc.get_transactions(uname, passwd)
    except Exception as e:
        print e
    finally:
        sc.close()

    if transactions:
        num_saved = store.save(transactions)

    print "Saved %d new transactions." % num_saved

if __name__ == '__main__':
    from_cmdline(ScraperClass=AllyScraper)
