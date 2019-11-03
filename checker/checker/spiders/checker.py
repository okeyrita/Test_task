# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from w3lib.html import remove_tags
import re
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
import sys

class CheckerSpider(scrapy.Spider):
    name = "checker"
    start_urls = [urljoin('https://opencorporates.com/companies/de/',re.sub('\n', '',sys.argv[1] ))]


    def parse(self, response):
        present_link = response.request.url
        check = response.css('.dialog.col-left p::text').get()
        if not(re.search("The page you were looking for doesn't exist.", check)):
            file = open('valid_id.txt', 'a')
            file.write(present_link+'\n')
            print('*')
            file.close()

if __name__ == "__main__":
    process = CrawlerProcess()
    settings = get_project_settings()
    process.crawl(CheckerSpider)
    process.start() # the script will block here until the crawling is finished
    process.stop()