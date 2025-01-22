# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class QuotePipeline:
    def __init__(self):
        self.i = 0
        self.create_connection()
        self.create_table()
        
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = os.getenv('DB_USER'),
            passwd = os.getenv('DB_PASSWORD'),
            database = 'Quotes'
        )
        self.cursor = self.conn.cursor()
        
    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS quotes_tb""")
        self.cursor.execute("""CREATE TABLE quotes_tb(
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(1000),
            author VARCHAR(200),
            tags VARCHAR(200)
        )""")
        self.cursor.execute("""DROP TABLE IF EXISTS tag_tb""")
        self.cursor.execute("""CREATE TABLE tag_tb(
            tag_id INT AUTO_INCREMENT PRIMARY KEY,
            tag_name VARCHAR(100),
            quote_id INT,
            FOREIGN KEY (quote_id) REFERENCES quotes_tb(id)
        )""")
    
    def store_db(self, item ):
        self.i += 1
        self.cursor.execute("""INSERT INTO quotes_tb VALUES (%s , %s, %s, %s)""", (
            self.i,
            item.get('title', [''])[0],
            item.get('author', [''])[0],
            ','.join(item.get('tags', []))
        ))
        self.conn.commit()
    def process_item(self, item, spider):
        self.store_db(item)
        return item
