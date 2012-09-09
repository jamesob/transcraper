import datetime
import time
import pprint

from .scraper import SeleniumScraper
from transcraper import Transaction

import logging
log = logging.getLogger(__name__)


class AllyScraper(SeleniumScraper):

    homepage_url = "http://www.ally.com"

    def __init__(self, username, password, cookies=None, secure_cookies=None):
        super(AllyScraper, self).__init__(username, password)

        self.cookies = cookies
        self.secure_cookies = secure_cookies

    def _login(self, username, password):
        """Return a logged-in Ally card selenium driver instance."""
        for c in self.cookies:
            self.driver.add_cookie(c)

        self.driver.get(self.homepage_url)
        time.sleep(1)

        l = self.driver.find_element_by_partial_link_text('log in')

        login_href = l.get_attribute('href')

        self.driver.get(login_href)
        time.sleep(2)

        for c in self.secure_cookies:
            self.driver.add_cookie(c)

        self.driver.get(login_href)
        time.sleep(2)

        inputElement = self.driver.find_element_by_id("username")
        inputElement.send_keys(username)
        inputElement.submit()
        time.sleep(2)

        inputElement = self.driver.find_element_by_name("password")
        inputElement.send_keys(password)
        inputElement.submit()
        time.sleep(2)

    def get_transactions(self, username, password):
        trans = []
        self._login(username, password)
        self._goto_link('Interest Checking')
        table = self.driver.find_element_by_class_name('ledgerTable')

        rows = table.find_elements_by_class_name('ledgerBackground1')
        rows += table.find_elements_by_class_name('ledgerBackground2')

        for row in rows:
            row = [td.text for td in row.find_elements_by_tag_name('td')]
            trans.append(self._row_to_transaction(row))

        pprint.pprint(trans)
        return trans

    def _row_to_transaction(self, row):
        occurred_at = datetime.datetime.strptime(row[0], '%m/%d/%Y')
        name = row[2]
        debit = row[3]
        credit = row[4]
        # balance = r[5]

        if debit:
            amount = self._clean_amount(debit)
        else:
            amount = '-%s' % (self._clean_amount(credit))

        return Transaction(name,
                           occurred_at=occurred_at,
                           amount=amount,
                           source=self.id)
