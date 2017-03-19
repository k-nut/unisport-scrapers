#!/bin/bash

rm data/*.json
source unisport_scrapers/bin/activate

scrapy crawl hu -o data/hu.json
scrapy crawl tu -o data/tu.json
scrapy crawl fu -o data/fu.json
scrapy crawl htw -o data/htw.json
scrapy crawl beuth -o data/beuth.json

python3 mergeSportsclasses.py
