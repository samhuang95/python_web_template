from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime
from bson import json_util
from src.configs.config import find_dotenv, generate_uuid
from src.models.article_model import ArticleModel

find_dotenv()
now = datetime.datetime.now()
# 创建 Blueprint
article_blueprint = Blueprint('article_blueprint', __name__)

db_name = os.getenv('DB_NAME')
mongodb_user = os.getenv('MONGODB_USER')
mongodb_password = os.getenv('MONGODB_PASSWORD')
mongodb_server = os.getenv('MONGODB_URL')

# MongoDB 设置
client = MongoClient(f'mongodb://{mongodb_user}:{mongodb_password}@{mongodb_server}/')
db = client['sam_web']
collection_name = 'articles'
collection = db[collection_name]

@article_blueprint.route('/article', methods=['POST'])
def create_article():
    data = request.json

    if not data or not isinstance(data, dict):
        return jsonify({'error': 'Invalid or missing JSON data'}), 400
    else:
        required_fields = ['title', 'eng_title', 'article_tag', 'statue', 'cover_url', 'summary', 'content']

        missing_or_empty_fields = [field for field in required_fields if not data.get(field)]

        if missing_or_empty_fields:
            return jsonify({'error': 'Missing or empty fields, pls check ["title", "eng_title", "article_tag", "statue", "cover_url", "summary", "content"]', 'details': missing_or_empty_fields}), 400
        else:
            input_data = {
                'article_id': generate_uuid(),
                'title': data['title'],
                'eng_title': data['eng_title'],
                'article_tag': data['article_tag'],
                'statue': data['statue'],
                'cover_url': data['cover_url'],
                'summary': data['summary'],
                'content': data['content'],
                'created_at': now,
                'updated_at': now
            }
            result = collection.insert_one(input_data)
            return jsonify(str(result.inserted_id)), 201

@article_blueprint.route('/article_list', methods=['GET'])
def get_article_list():
    article_id = request.args.get('article_id')

    if not article_id:
        records = collection.find({})
        if records:
            return json_util.dumps([record for record in records]), 200, {'Content-Type': 'application/json'}
        else:
            return jsonify({'error': 'Article not found'}), 404
    else:
        record = collection.find_one({'article_id': article_id})
        if record:

            return json_util.dumps(record), 200, {'Content-Type': 'application/json'}
        else:
            return jsonify({'error': 'Article not found'}), 404

@article_blueprint.route('/article', methods=['PATCH'])
def update_record():
    article_id = request.args.get('article_id')

    if not article_id:
        return jsonify({'error': 'Article ID not found'}), 404
    else:
        data = request.json

        result = collection.update_one({'article_id': article_id}, {'$set': data})
        return jsonify(str(result.modified_count)), 200

@article_blueprint.route('/article', methods=['DELETE'])
def delete_record():
    article_id = request.args.get('article_id')
    if not article_id:
        return jsonify({'error': 'Article ID not found'}), 404
    else:
        result = collection.delete_one({'article_id': article_id})
        return jsonify(str(result.deleted_count)), 200
