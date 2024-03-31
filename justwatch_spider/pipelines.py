# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2

class JustwatchSpiderPipeline:
    def process_item(self, item, spider):
        return item

class SavingSortingsToPostgresPipeline(object):

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost", database="postgres", user="rohits"
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()



        # Drop existing data
        self.cur.execute("DROP TABLE IF EXISTS sorted_by_imdb_score;")
        self.cur.execute("DROP TABLE IF EXISTS sorted_by_popularity;")
        self.cur.execute("DROP TABLE IF EXISTS sorted_by_tmdb_popularity;")

        ## Create table
        self.cur.execute("""
        CREATE TABLE sorted_by_imdb_score(
            rank SERIAL PRIMARY KEY, 
            title TEXT
        );
        """)
        ## Create table
        self.cur.execute("""
        CREATE TABLE sorted_by_popularity(
            rank SERIAL PRIMARY KEY, 
            title TEXT
        );
        """)
        ## Create table
        self.cur.execute("""
        CREATE TABLE sorted_by_tmdb_popularity(
            rank SERIAL PRIMARY KEY, 
            title TEXT
        );
        """)

        self.conn.commit()


    def process_item(self, item, spider):

        if item["SORTED BY"] == "IMDB_SCORE":
            self.cur.execute(f"INSERT INTO sorted_by_imdb_score (title) VALUES ('{item["TITLE"].replace("'", "''")}');")

        if item["SORTED BY"] == "POPULAR":
            self.cur.execute(f"INSERT INTO sorted_by_popularity (title) VALUES ('{item["TITLE"].replace("'", "''")}');")

        if item["SORTED BY"] == "TMDB_POPULARITY":
            self.cur.execute(f"INSERT INTO sorted_by_tmdb_popularity (title) VALUES ('{item["TITLE"].replace("'", "''")}');")


        self.conn.commit()
        return item

    def close_spider(self, spider):
        # # Close cursor & connection to database
        self.cur.close()
        self.conn.close()
