import datetime
import time

from .scraper import SeleniumScraper
from transcraper import Transaction

import logging
log = logging.getLogger(__name__)


class ChaseScraper(SeleniumScraper):

    homepage_url = "http://www.chase.com"

    def get_transactions(self, username, password):
        log.info("Initiating scrape for ChaseScraper.")
        rows = self._get_activity(username, password)

        log.info("Got %d rows from scraping." % len(rows))
        return self._raw_rows_to_transactions(rows)

    def _raw_rows_to_transactions(self, rs):
        return [self._raw_row_to_transaction(r) for r in rs]

    def _raw_row_to_transaction(self, r):
        """
        Take a row scraped directly from Chase and turn it into a Transaction.

        Row assumed to be in the following format:
            [u'08/18/2012', u'08/20/2012', u'Sale',
             u'NITEHAWK CINEMA THEATR', u'', u'$32.00']
        """
        occurred_at = datetime.datetime.strptime(r[0], '%m/%d/%Y')
        amount = self._clean_amount(r[5])

        return Transaction(name=r[3],
                           occurred_at=occurred_at,
                           amount=amount,
                           source=self.id)

    def _login(self, username, password):
        """Log in with selenium."""
        time.sleep(2)

        inputElement = self.driver.find_element_by_id("usr_name")
        inputElement.send_keys(username)

        pwdElement = self.driver.find_element_by_id("usr_password")
        pwdElement.send_keys(password)

        pwdElement.submit()

    def _get_recent_activity_rows(self):
        """Return the 25 most recent CC transactions, plus any pending
        transactions.

        Returns:
            A list of lists containing the columns of the Chase transaction
            list.
        """
        self._goto_link("See activity")
        time.sleep(2)

        rows = self.driver.find_elements_by_css_selector("tr.summary")
        trans_list = []

        for row in rows:
            tds = row.find_elements_by_tag_name('td')
            tds = tds[1:]  # skip the link in first cell
            trans_list.append([td.text for td in tds])

        return trans_list

    def _get_activity(self, username, password):
        """For a given username, retrieve recent account activity for
        a Chase CC."""
        rows = None
        self._login(username, password)
        time.sleep(4)

        try:
            rows = self._get_recent_activity_rows()
        except Exception, e:
            print e
        finally:
            self.driver.quit()

        return rows
