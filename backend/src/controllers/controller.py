import datetime
from flask import request, jsonify
from src.models.article_model import ArticleModel
from bson import json_util

now = datetime.datetime.now()
article_model = ArticleModel()

def create_article():
    article_data = request.json
    if not article_data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400
    else:
        required_fields = ['title', 'eng_title', 'article_tag', 'statue', 'cover_url', 'summary', 'content']
        missing_or_empty_fields = [field for field in required_fields if not article_data.get(field)]

        if missing_or_empty_fields:
            return jsonify({'error': 'Missing or empty fields, pls check ["title", "eng_title", "article_tag", "statue", "cover_url", "summary", "content"]', 'details': missing_or_empty_fields}), 400
        else:
            result = article_model.create_article(article_data)
            return jsonify({'_id': str(result.inserted_id)}), 201

def get_article_list():
    article_id = request.args.get('article_id')
    if not article_id:
        article_list = article_model.get_article_list()
        if not article_list:
            return jsonify({'error': 'Article list not found'}), 404
        else:
            return json_util.dumps([record for record in article_list]), 200, {'Content-Type': 'application/json'}
    else:
        article = article_model.get_article(article_id)
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        else:
            return json_util.dumps(article), 200, {'Content-Type': 'application/json'}

def update_record():
    article_id = request.args.get('article_id')
    if not article_id:
        return jsonify({'error': 'Article ID not provided'}), 400
    else:
        update_data = request.json

    if not update_data:
        return jsonify({'error': 'No update data provided'}), 400
    else:
        result = article_model.update_article(article_id, update_data)
        return jsonify({'updated message(success:1/ fail:0):': result.modified_count}), 200

def delete_record():
    article_id = request.args.get('article_id')
    if not article_id:
        return jsonify({'error': 'Article ID not provided'}), 400
    else:
        result = article_model.delete_article(article_id)
        return jsonify({'deleted message(success:1/ fail:0):': result.deleted_count}), 200
