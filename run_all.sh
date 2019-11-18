#!/bin/bash

# exit on first failure
set -e

dropdb unisport && createdb unisport && python create_db.py
scrapy list | xargs -n 1 scrapy crawl
