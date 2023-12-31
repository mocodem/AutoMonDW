import peewee
from peewee import *
import datetime
import sqlite3
from elasticsearch import Elasticsearch

# Establish connection to Elasticsearch
es = Elasticsearch("http://localhost:9200")

def drop():
    # Drop the Onion table from the database
    sure = input("Sure to drop all data?")
    if sure == "y":
        connection = sqlite3.connect('onion.db')
        connection.execute("DROP TABLE Onion")
        print("data dropped")
        connection.close()

# Define the database
db = SqliteDatabase('onion.db')

class BaseModel(Model):
    class Meta:
        database = db

class Onion(BaseModel):
    # Define fields for the Onion table
    url = CharField()
    source = CharField()
    url_version = CharField(null=True)
    title = CharField(null=True)
    status = IntegerField(null=True)
    connect = CharField(null=True)
    captcha = BooleanField(null=True)
    captcha_type = CharField(null=True)
    first_itc = DateTimeField()
    last_itc = DateTimeField(default=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))

    class Meta:
        primary_key = CompositeKey('url', 'source')

class Sitemap(BaseModel):
    # Define fields for the Sitemap table
    sub = CharField()
    itc = DateTimeField(default=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    collected = BooleanField(null=True)
    url = ForeignKeyField(Onion, to_field='url')

class Content(BaseModel):
    # Define fields for the Content table
    content = CharField()
    itc = DateTimeField(default=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    url = ForeignKeyField(Onion, to_field='url')
    sub = ForeignKeyField(Sitemap, to_field='sub')

def init_db():
    # Initialize the database and create tables
    db.connect()
    Onion.create_table()
    Sitemap.create_table()
    db.close()

def add_onion(url: str, source: str, title: str = None) -> bool:
    # Add an onion to the Onion table
    try:
        query = Onion.create(url=url, source=source, first_itc=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                             last_itc=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        query.url_version = check_url_verison(url)
        query.save()
        return True
    except peewee.IntegrityError as e:
        query = get_onion_source(url=url, source=source)
        query.last_itc = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        query.save()
        return True

def add_sitemap(sub: str, url: str, collected: bool = False) -> bool:
    # Add a sitemap to the Sitemap table
    query = Sitemap.create(sub=sub, url=url)
    query.save()
    return True

def sanitize_url(url: str) -> str:
    # Sanitize the URL by removing fragments and adding ".onion" if necessary
    if len(url.split(".onion/")) > 1:
        return url.split(".onion/")[0] + ".onion"
    elif ".onion" not in url:
        return url + ".onion"
    else:
        return url

def check_url_verison(url: str) -> str:
    # Check the version of the URL (v2 or v3)
    url_version = url
    if ".onion" in url_version:
        url_version = url_version.split(".onion")[0]
    if "http://" in url_version:
        url_version = url_version.split("http://")[1]
    elif "https://" in url_version:
        url_version = url_version.split("https://")[1]
    if "www." in url_version:
        url_version = url_version.split("www.")[1]
    if len(url_version) == 56:
        url_version = "v3"
    elif len(url_version) == 16:
        url_version = "v2"
    else:
        url_version = "unknown"
    return url_version

def get_onion(url: str) -> Onion:
    # Get an Onion record by URL
    try:
        return Onion.get(Onion.url == url)
    except Onion.DoesNotExist as e:
        return None

def get_onion_source(url: str, source: str) -> Onion:
    # Get an Onion record by URL and source
    return Onion.get(Onion.url == url, Onion.source == source)

def get_all_onions() -> [Onion]:
    # Get all Onion records
    query = Onion.select()
    all_onions = [onion.url for onion in query]
    all_onions = list(set(all_onions))
    return all_onions

def get_all_onions_v3() -> [Onion]:
    # Get all Onion records with URL version v3
    query = Onion.select().where(Onion.url_version == "v3")
    all_onions = [onion.url for onion in query]
    all_onions = list(set(all_onions))
    return all_onions

def get_all_onions_v3_source() -> [Onion]:
    # Get all Onion records with URL version v3 and their sources
    query = Onion.select().where(Onion.url_version == "v3")
    all_onions = [(onion.url, onion.source) for onion in query]
    return all_onions

def get_all_onions_status(status: int) -> [Onion]:
    # Get all Onion records with a specific status
    query = Onion.select().where(Onion.status == status)
    all_onions = [onion.url for onion in query]
    all_onions = list(set(all_onions))
    return all_onions

def get_all_onions_captcha(captcha: bool) -> [Onion]:
    # Get all Onion records with a specific captcha status
    query = Onion.select().where(Onion.captcha == captcha)
    all_onions = [onion.url for onion in query]
    all_onions = list(set(all_onions))
    return all_onions

def update_onion(url: str, key: str, value) -> bool:
    # Update a specific field of an Onion record
    query = Onion.get(Onion.url == url)
    query.key = value
    query.save()
    return True

try:
    init_db()
    print("DB successfully initialized")
except:
    input("DB is not initialized, continue? ")
