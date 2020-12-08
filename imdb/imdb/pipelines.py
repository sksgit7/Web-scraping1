# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymongo
import sqlite3

class MongodbPipeline(object):
    collection_name='best_movies'

    #@classmethod
    # def from_crawler(cls,crawler): # grab elements from settings.py
    #     logging.warning(crawler.settings.get("MONGO_URI"))

    def open_spider(self,spider):
        self.client=pymongo.MongoClient("mongodb+srv://subham:1234567890@cluster0.cz1nh.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.db= self.client["IMDB"]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item) # store scraped element in db
        return item

class SQLlitePipeline(object):
    

    #@classmethod
    # def from_crawler(cls,crawler): # grab elements from settings.py
    #     logging.warning(crawler.settings.get("MONGO_URI"))

    def open_spider(self,spider):
        self.connection= sqlite3.connect('imdb.db')
        self.c= self.connection.cursor() # create cursor
        
        try:
            self.c.execute('''
                CREATE TABLE best_movies(
                    title TEXT,
                    year TEXT,
                    duration TEXT,
                    genre TEXT,
                    rating TEXT,
                    movie_url TEXT
                )
            ''')
        except sqlite3.OperationalError:
            pass
        self.connection.commit()

    def close_spider(self,spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO best_movies(title, year, duration, genre, rating, movie_url) VALUES (?,?,?,?,?,?)
        ''',(
            item.get('title'),
            item.get('year'),
            item.get('duration'),
            item.get('genre'),
            item.get('rating'),
            item.get('movie_url'),
        )) # store scraped element in db

        self.connection.commit()
        return item
