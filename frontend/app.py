from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', message="這是一個測試消息", pp='This is a test')

@app.route('/hello')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)