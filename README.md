# unisport-scrapers

Scrapers for all sports classes offered by universities in Berlin.

## Installation

Create a new virtualen environment with `virtualenv unisport-scrapers -p /usr/local/bin/python3`, activate it via `source unisport-scrapers/bin/activate`  and install the requirements with `pip install -r requirements.txt`


## Running
You can run an individual scraper via `scrapy crawl hu -o hu.json` or run a script that runs all scrapers and merges their results in 
a file called `alle.json` by running `run_all.sh`
