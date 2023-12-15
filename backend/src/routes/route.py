from flask import Blueprint
from src.controllers.article_controller import create_article, get_article_list, update_record, delete_record

article_blueprint = Blueprint('article_blueprint', __name__)

article_blueprint.route('/article', methods=['POST'])(create_article)
article_blueprint.route('/article_list', methods=['GET'])(get_article_list)
article_blueprint.route('/article', methods=['PATCH'])(update_record)
article_blueprint.route('/article', methods=['DELETE'])(delete_record)