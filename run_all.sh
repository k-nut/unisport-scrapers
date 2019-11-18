#!/bin/bash

# exit on first failure
set -e

python empty_db.py
scrapy list | xargs -n 1 scrapy crawl
