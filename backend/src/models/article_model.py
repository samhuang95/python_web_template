import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from src.configs.config import generate_uuid

load_dotenv()
class ArticleModel:

    def __init__(self):
        # Get the MongoDB URL from the.env file
        db_name = os.getenv('DB_NAME')
        mongodb_user = os.getenv('MONGODB_USER')
        mongodb_password = os.getenv('MONGODB_PASSWORD')
        mongodb_server = os.getenv('MONGODB_URL')

        # Connect to MongoDB
        client = MongoClient(f'mongodb://{mongodb_user}:{mongodb_password}@{mongodb_server}/')
        db = client[db_name]
        self.collection = db['articles']


    def get_article_list(self)-> list:
        return self.collection.find({})

    def get_article(self, article_id:str) -> dict:
        return self.collection.find_one({'article_id': article_id})

    def create_article(self, article:dict):
        now = datetime.datetime.now()
        data = {
            'article_id': generate_uuid(),
            'title': article['title'],
            'eng_title': article['eng_title'],
            'article_tag': article['article_tag'],
            'statue': article['statue'],
            'cover_url': article['cover_url'],
            'summary': article['summary'],
            'content': article['content'],
            'created_at': now,
            'updated_at': now
        }

        return self.collection.insert_one(data)

    def update_article(self, article_id:str, update_data:object):
        now = datetime.datetime.now()
        update_data['updated_at'] = now
        return self.collection.update_one({'article_id': article_id}, {'$set': update_data})

    def delete_article(self, article_id):
        return self.collection.delete_one({'article_id': article_id})
