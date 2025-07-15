# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import pycountry
from utils import expand_genre

# class JustwatchSpiderPipeline:
#     def process_item(self, item, spider):
#         return item

class SavingSortingsToPostgresPipeline(object):

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost", database="postgres", user="rohit"
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
            id TEXT,
            title TEXT,
            year INTEGER
        );
        """)
        ## Create table
        self.cur.execute("""
        CREATE TABLE sorted_by_popularity(
            rank SERIAL PRIMARY KEY, 
            id TEXT,
            title TEXT,
            year INTEGER
        );
        """)
        ## Create table
        self.cur.execute("""
        CREATE TABLE sorted_by_tmdb_popularity(
            rank SERIAL PRIMARY KEY, 
            id TEXT,
            title TEXT,
            year INTEGER
        );
        """)

        self.conn.commit()


    def process_item(self, item, spider):

        if item["SORTED BY"] == "IMDB_SCORE":
            self.cur.execute(f"INSERT INTO sorted_by_imdb_score (id, title, year) VALUES ('{item["ID"]}', '{item["TITLE"].replace("'", "''")}', '{item["YEAR"]}');")

        if item["SORTED BY"] == "POPULAR":
            self.cur.execute(f"INSERT INTO sorted_by_popularity (id, title, year) VALUES ('{item["ID"]}', '{item["TITLE"].replace("'", "''")}', '{item["YEAR"]}');")

        if item["SORTED BY"] == "TMDB_POPULARITY":
            self.cur.execute(f"INSERT INTO sorted_by_tmdb_popularity (id, title, year) VALUES ('{item["ID"]}', '{item["TITLE"].replace("'", "''")}', '{item["YEAR"]}');")


        self.conn.commit()
        return item

    def close_spider(self, spider):
        # # Close cursor & connection to database
        self.cur.close()
        self.conn.close()



def serialize_null(value):
    if not value or value == 'null':
        return 0
    return value

class SavingWatchListToPostgresPipeline(object):

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost", database="postgres", user="rohit"
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        # Drop existing data
        self.cur.execute("DROP TABLE IF EXISTS watchlist CASCADE;")
        self.cur.execute("DROP TABLE IF EXISTS seenlist CASCADE;")
        self.cur.execute("DROP TABLE IF EXISTS countries CASCADE;")
        self.cur.execute("DROP TABLE IF EXISTS directors CASCADE;")
        self.cur.execute("DROP TABLE IF EXISTS genres CASCADE;")
        self.cur.execute("DROP TABLE IF EXISTS casts CASCADE;")
        self.cur.execute("DROP TABLE IF EXISTS movie_cast CASCADE;")
        self.cur.execute("DROP TABLE IF EXISTS movie_directors CASCADE;")
        self.cur.execute("DROP TABLE IF EXISTS movie_genres CASCADE;")
        self.cur.execute("DROP TABLE IF EXISTS movie_countries CASCADE;")

        self.cur.execute("""
        CREATE TABLE watchlist(
            id TEXT PRIMARY KEY, 
            title TEXT,
            runtime REAL,
            year INTEGER,
            object_type TEXT,
            imdb_score REAL,
            imdb_votes INTEGER,
            tmdb_score REAL,
            tmdb_popularity REAL,
            popularity_rank INTEGER,
            jw_rating REAL
        );
        """)

        self.cur.execute("""
        CREATE TABLE seenlist(
            id TEXT PRIMARY KEY, 
            title TEXT,
            runtime REAL,
            year INTEGER,
            object_type TEXT,
            imdb_score REAL,
            imdb_votes INTEGER,
            tmdb_score REAL,
            tmdb_popularity REAL,
            popularity_rank INTEGER,
            jw_rating REAL
        );
        """)

        self.cur.execute("""
        CREATE TABLE countries(
            id TEXT PRIMARY KEY, 
            name TEXT
        );
        """)

        self.cur.execute("""
        CREATE TABLE genres(
            name TEXT PRIMARY KEY 
        );
        """)

        self.cur.execute("""
        CREATE TABLE directors(
            name TEXT PRIMARY KEY 
        );
        """)

        self.cur.execute("""
        CREATE TABLE casts(
            name TEXT PRIMARY KEY 
        );
        """)

        self.cur.execute("""
        CREATE TABLE movie_cast(
            name TEXT NOT NULL,
            movie TEXT NOT NULL,
            reference_type TEXT NOT NULL,
            FOREIGN KEY (name) REFERENCES casts(name),
            PRIMARY KEY (name, movie)
        );
        """)

        self.cur.execute("""
        CREATE TABLE movie_countries(
            country_id TEXT NOT NULL, 
            movie TEXT NOT NULL,
            reference_type TEXT NOT NULL,
            FOREIGN KEY (country_id) REFERENCES countries(id),
            PRIMARY KEY (country_id, movie)
        );
        """)

        self.cur.execute("""
        CREATE TABLE movie_directors(
            name TEXT NOT NULL, 
            movie TEXT NOT NULL,
            reference_type TEXT NOT NULL,
            FOREIGN KEY (name) REFERENCES directors(name),
            PRIMARY KEY (name, movie)
        );
        """)

        self.cur.execute("""
        CREATE TABLE movie_genres(
            name TEXT NOT NULL, 
            movie TEXT NOT NULL,
            reference_type TEXT NOT NULL,
            FOREIGN KEY (name) REFERENCES genres(name),
            PRIMARY KEY (name, movie)
        );
        """)

        self.conn.commit()


    def process_item(self, item, spider):

        if item["list_type"] == "WATCHLIST":
            self.cur.execute(f"INSERT INTO watchlist VALUES ('{item["id"]}', '{item["title"].replace("'", "''")}', {item["runtime"]}, {item["year"]}, '{item["object_type"]}', {serialize_null(item["imdb_score"])}, {serialize_null(item["imdb_votes"])}, {serialize_null(item["tmdb_score"])}, {item["tmdb_popularity"]}, {item["popularity_rank"]}, {serialize_null(item["jw_rating"])});")
        else:
            self.cur.execute(f"INSERT INTO seenlist VALUES ('{item["id"]}', '{item["title"].replace("'", "''")}', {item["runtime"]}, {item["year"]}, '{item["object_type"]}', {serialize_null(item["imdb_score"])}, {serialize_null(item["imdb_votes"])}, {serialize_null(item["tmdb_score"])}, {item["tmdb_popularity"]}, {item["popularity_rank"]}, {serialize_null(item["jw_rating"])});")

        for country in item["countries"]:
            if country.lower() == 'su':
                country = 'ru'
            self.cur.execute(f"INSERT INTO countries VALUES ('{country}', '{pycountry.countries.lookup(country).name}') ON CONFLICT (id) DO NOTHING;")
            self.cur.execute(f"INSERT INTO movie_countries VALUES('{country}', '{item["id"]}', '{item["list_type"]}') ON CONFLICT (country_id, movie) DO NOTHING;")

        for c in item["credits"]:
            if c['role'] == 'DIRECTOR':
                self.cur.execute(f"INSERT INTO directors VALUES ('{c["name"].replace("'", "''")}') ON CONFLICT (name) DO NOTHING;")
                self.cur.execute(f"INSERT INTO movie_directors VALUES('{c["name"].replace("'", "''")}', '{item["id"]}', '{item["list_type"]}') ON CONFLICT (name, movie) DO NOTHING;")
            else:
                self.cur.execute(f"INSERT INTO casts VALUES ('{c["name"].replace("'", "''")}') ON CONFLICT (name) DO NOTHING;")
                self.cur.execute(f"INSERT INTO movie_cast VALUES('{c["name"].replace("'", "''")}', '{item["id"]}', '{item["list_type"]}') ON CONFLICT (name, movie) DO NOTHING;")

        for genre in item["genres"]:
            g = expand_genre(genre["shortName"]) 
            self.cur.execute(f"INSERT INTO genres VALUES ('{g}') ON CONFLICT (name) DO NOTHING;")
            self.cur.execute(f"INSERT INTO movie_genres VALUES('{g}', '{item["id"]}', '{item["list_type"]}') ON CONFLICT (name, movie) DO NOTHING;")

        self.conn.commit()
        return item

    def close_spider(self, spider):
        # # Close cursor & connection to database
        self.cur.close()
        self.conn.close()





class SavingHindiListToPostgresPipeline(object):

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost", database="postgres", user="rohit"
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        # Drop existing data
        self.cur.execute("DROP TABLE IF EXISTS hindi_confirmed;")

        ## Create table
        self.cur.execute("""
        CREATE TABLE hindi_confirmed(
            title TEXT PRIMARY KEY
        );
        """)
        self.conn.commit()


    def process_item(self, item, spider):

        self.cur.execute(f"INSERT INTO hindi_confirmed (title) VALUES ('{item["TITLE"].replace("'", "''")}');")
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # # Close cursor & connection to database
        self.cur.close()
        self.conn.close()



class SavingHotListToPostgresPipeline(object):

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost", database="postgres", user="rohit"
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        # Drop existing data
        self.cur.execute("DROP TABLE IF EXISTS hot_list;")

        ## Create table
        self.cur.execute("""
        CREATE TABLE hot_list(
            title TEXT PRIMARY KEY
        );
        """)
        self.conn.commit()


    def process_item(self, item, spider):

        self.cur.execute(f"INSERT INTO hot_list (title) VALUES ('{item["TITLE"].replace("'", "''")}');")
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # # Close cursor & connection to database
        self.cur.close()
        self.conn.close()
