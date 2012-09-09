from selenium import webdriver
import datetime
import time

from .scraper import Scraper
from transcraper import Transaction

import logging
log = logging.getLogger(__name__)


class ChaseAmazon(Scraper):

    def get_transactions(self, username, password):
        log.info("Initiating scrape for ChaseAmazon.")
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
        amount = r[5].replace('$', '')

        return Transaction(name=r[3],
                           occurred_at=occurred_at,
                           amount=amount,
                           source=self.id)

    def _get_chase_amazon_driver(self, username, password):
        """Return a logged-in Chase Amazon card selenium driver instance."""
        driver = webdriver.Firefox()
        driver.get("http://www.chase.com")

        time.sleep(2)

        inputElement = driver.find_element_by_id("usr_name")
        inputElement.send_keys(username)

        pwdElement = driver.find_element_by_id("usr_password")
        pwdElement.send_keys(password)

        pwdElement.submit()
        return driver

    def _goto_link(self, driver, text):
        """Follow a link with a WebDriver."""
        l = driver.find_element_by_partial_link_text(text)
        driver.get(l.get_attribute('href'))

    def _get_recent_activity_rows(self, chase_driver):
        """Return the 25 most recent CC transactions, plus any pending
        transactions.

        Returns:
            A list of lists containing the columns of the Chase transaction
            list.
        """
        self._goto_link(chase_driver, "See activity")

        rows = chase_driver.find_elements_by_css_selector("tr.summary")
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
        d = self._get_chase_amazon_driver(username, password)
        time.sleep(8)

        try:
            rows = self._get_recent_activity_rows(d)
        except Exception, e:
            print e
        finally:
            d.quit()

        return rows
