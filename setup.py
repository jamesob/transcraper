#!/usr/bin/env python

from distutils.core import setup

setup(name='transcraper',
      version='0.1',
      description='Scrape transaction data from financial institutions',
      author="James O'Beirne",
      author_email='james.obeirne@gmail.com',
      url='https://github.com/jamesob/transcrape',
      packages=['transcraper'],
      requires=['pymongo', 'selenium'],
      )
