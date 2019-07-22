#!/bin/bash

# exit on first failure
set -e

# change to script directory
cd "$(dirname "$0")"

rm data/*.json || true
source unisport-scrapers/bin/activate

scrapy crawl hu -o data/hu.json
scrapy crawl tu -o data/tu.json
scrapy crawl fu -o data/fu.json
scrapy crawl htw -o data/htw.json
scrapy crawl beuth -o data/beuth.json
scrapy crawl potsdam -o data/potsdam.json

python3 mergeSportsclasses.py
