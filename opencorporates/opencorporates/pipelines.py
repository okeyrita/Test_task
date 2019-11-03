# -*- coding: utf-8 -*-
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
import pymongo


class MongoDBPipeline(object):
    writeTypes = [
        'company_information', 'latest_events',
        'similarly_named_companies', 'director_information',
        'similarly_named_officers'
    ]

    def open_spider(self, spider):
        SETTINGS = get_project_settings()
        self.connection = pymongo.MongoClient(
            SETTINGS['MONGODB_SERVER'],
            SETTINGS['MONGODB_PORT']
        )
        self.database = self.connection[SETTINGS['MONGODB_DB']]
        self.collections = dict([(name, self.database[name])
                                 for name in self.writeTypes])

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        if item['type'] == 'company_information':
            self.collections['company_information'].update(item, item, True)
        elif item['type'] == 'latest_events':
            self.collections['latest_events'].update(item, item, True)
        elif item['type'] == 'similarly_named_companies':
            self.collections['similarly_named_companies'].update(
                item, item, True)
        elif item['type'] == 'director_information':
            self.collections['director_information'].update(item, item, True)
        elif item['type'] == 'similarly_named_officers':
            self.collections['similarly_named_officers'].update(
                item, item, True)
        else:
            raise DropItem('Item type is unknown')

        return item
