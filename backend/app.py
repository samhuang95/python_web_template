from flask import Flask
from dotenv import load_dotenv
from src.routes.route import article_blueprint

load_dotenv()

app = Flask(__name__)
app.register_blueprint(article_blueprint, url_prefix='/read')

@app.route('/')
def index():
    return "Welcome to the CRUD API!"

if __name__ == '__main__':
    app.run(debug=True)