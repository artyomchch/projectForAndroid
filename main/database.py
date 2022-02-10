# Create the client
import datetime

from pymongo import MongoClient


def config_db():
    client = MongoClient('localhost', 27017)
    db = client['apps']
    series_collection = db['test_apps']
    post = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}

    posts = db.posts
    post_id = posts.insert_one(post).inserted_id



config_db()
