# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from w3lib.html import remove_tags
import re
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
import json
import sys


class OpenCorpSpider(scrapy.Spider):
    name = "opencorp"
    # choose all id-s from file valid_id_from_site.txt for parsing
    with open('valid_id_from_site.txt', 'r') as input_file:
        lines = input_file.readlines()
        start_urls = []
        for line in lines:
            start_urls.append(urljoin(
                'https://opencorporates.com/companies/de/', re.sub('\n', '', line)))

    def __init__(self, *args, **kwargs):
        # for control duplicating information
        self.parsed_officers_links = set()
        self.parsed_companies_links = set()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(OpenCorpSpider, cls).from_crawler(
            crawler, *args, **kwargs)

        return spider

    def parse_similarly_named_officers(self, response):
        table = response.css('div ul')
        # Similarly named officers (information from this section,
        # with link and names of the company form each link)
        lines = table.css('li')
        for line in lines:
            if line.css('.officer::text').get() != None:
                company_link = urljoin(
                    'https://opencorporates.com/', line.css('.company::attr(href)').get())

                yield{
                    'type': 'similarly_named_officers',
                    'name': line.css('.officer::text').get(),
                    'link': urljoin('https://opencorporates.com/', line.css('.officer::attr(href)').get()),
                    'position': re.sub('\n', '', re.sub(',', '', line.css('::text').get())),
                    'company_name': line.css('.company::text').get(),
                    'company_link': company_link,
                }

                for link in self.parsed_companies_links:
                    if not (link == company_link):
                        yield response.follow(company_link, self.parse)

        # parse all available pages
        next_page = response.css(
            '.pagination.next.next_page a::attr(href)').get()
        if next_page != None:
            yield response.follow(urljoin('https://opencorporates.com/', next_page), self.parse_similarly_named_officers)

    def parse_officers(self, response):
        # parse Director information
        current_link = response.request.url
        table = response.css('.attributes')
        company = table.css('.company a::text').get()
        name = table.css('.name a::text').get()
        address = table.css('.address a::text').get()
        if address == 'Sorry, you need to be logged in to see this address':
            address = ''
        position = table.css('.position::text').get()
        start_date = table.css('.start_date::text').get()
        end_date = table.css('.end_date::text').get()
        similarly_named_officers_link = response.css(
            '.sidebar h3 a::attr(href)').get()

        yield{
            'type': 'director_information',
            'link': current_link,
            'company': company,
            'name': name,
            'address': address,
            'position': position,
            'start_date': start_date,
            'end_date': end_date,
        }
        self.parsed_officers_links.add(current_link)
        if similarly_named_officers_link != None:
            yield response.follow(similarly_named_officers_link, self.parse_similarly_named_officers)

    def parse(self, response):
        current_link = response.request.url
        # parse Company Information
        table = response.css('.attributes.dl-horizontal')
        company_number = table.css(
            '.company_number::text').get()  # 1 Company Number
        native_company_number = table.css(
            '.native_company_number a::text').get()  # 2 Native Company Number
        status = table.css('.status::text').get()  # 3 Status
        jurisdiction = table.css(
            '.jurisdiction a::text').get()  # 4 Jurisdiction
        registered_address = ''.join(
            table.css('.address_line::text').getall())  # 5 Registered Address
        previous_names = table.css(
            '.name_line::text').getall()  # 6 Previous Names

        # 7 Find Directors / Officers and 8 Inactive Directors / Officers
        officers_links = []
        directors_officers = []
        inactive_directors_officers = []
        directors_officers_all = table.css('.attribute_item')
        for dir in directors_officers_all:

            if dir.css('.officer.inactive::text').get() != None:  # choose inactive officers
                directors_officers_name = dir.css(
                    '.officer.inactive::text').get()
                directors_officers_link = dir.css(
                    '.officer.inactive::attr(href)').get()

                info = ''.join([str(dir.css('.start_date::text').get()),
                                '-', str(dir.css('.end_date::text').get())])

                inactive_directors_officers.append({  # 8 Inactive Directors / Officers
                    'name': directors_officers_name,
                    'link': urljoin('https://opencorporates.com/', directors_officers_link),
                    'position': re.sub('-', '', re.sub(', ', '', str(dir.css('li::text').get()))),
                    'info': info,
                })
                officers_links.append(
                    urljoin('https://opencorporates.com/', directors_officers_link))
            elif dir.css('.officer::text').get() != None:  # choose active officers
                directors_officers_name = dir.css('.officer::text').get()
                directors_officers_link = dir.css('.officer::attr(href)').get()

                info = ''.join([str(dir.css('.start_date::text').get()),
                                '-', str(dir.css('.end_date::text').get())])

                directors_officers.append({  # 7 Directors / Officers
                    'name': directors_officers_name,
                    'link': urljoin('https://opencorporates.com/', directors_officers_link),
                    'position': re.sub('-', '', re.sub(', ', '', str(dir.css('li::text').get()))),
                    'info': info,
                })
                officers_links.append(
                    urljoin('https://opencorporates.com/', directors_officers_link))
        # find Latest events
        events = response.css('.sidebar dl')
        latest_events_date = events.css('dt::text').getall()
        latest_events_event = events.css('dd a::text').getall()
        latest_events_link = events.css('dd a::attr(href)').getall()
        if latest_events_date != []:
            for date, event, link in zip(latest_events_date, latest_events_event, latest_events_link):
                yield{
                    'type': 'latest_events',
                    'company_number': company_number,
                    'date': re.sub('\n', '', date),
                    'event': event,
                    'link': urljoin('https://opencorporates.com/', link),
                }

        # find Similarly named companies of current company
        similarly = response.css('.sidebar li')
        similarly_named_companies_name = similarly.css('a::text').getall()
        similarly_named_companies_link = similarly.css(
            'a::attr(href)').getall()
        for link in similarly_named_companies_link:
            if not(re.search('/companies/\S{1,}/\S{1,}', link)):
                similarly_named_companies_link.remove(link)
        for name, link in zip(similarly_named_companies_name, similarly_named_companies_link):
            yield{
                'type': 'similarly_named_companies',
                'company_number': company_number,
                'name': name,
                'link': urljoin('https://opencorporates.com/', link),
            }

        yield {
            'type': 'company_information',
            'company_number': company_number,
            'native_company_number': native_company_number,
            'status': status,
            'jurisdiction': jurisdiction,
            'registered_address': registered_address,
            'previous_names': previous_names,
            'directors_officers': directors_officers,
            'inactive_directors_officers': inactive_directors_officers,
            'link': current_link,
        }
        self.parsed_companies_links.add(current_link)

        # After we have collected information about the companies, we need to collect
        # information about the officers who were in positions in these companies.
        for link in officers_links:
            if len(self.parsed_officers_links) != 0:
                for parsed_officer in self.parsed_officers_links:
                    if parsed_officer != link:
                        yield response.follow(link, self.parse_officers)
            else:
                yield response.follow(link, self.parse_officers)
