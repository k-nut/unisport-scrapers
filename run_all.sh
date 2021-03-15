#!/bin/bash

# exit on first failure
set -e

python empty_db.py
for name in $(scrapy list)
do
  echo "----- Scraping $name --------"
  scrapy crawl --loglevel=INFO $name
  echo "---------- Done -------------"
  echo
done
