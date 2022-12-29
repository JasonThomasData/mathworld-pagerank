#!/usr/bin/env python3

from web_browser import Browser
from page_parser import Parser
from db_manager import DBManager
from db_model import DB_MODEL
from web_crawler import Crawler

url_no_path = "https://mathworld.wolfram.com"
seed_url = "https://mathworld.wolfram.com"
db_name = "network-data.db"

browser = Browser()
parser = Parser()
db_manager = DBManager(db_name)
crawler = Crawler(url_no_path, seed_url, browser, parser, db_manager)

crawler.crawl()


