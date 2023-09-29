from flask import Flask, render_template
from flask_cors import CORS
from api.v1.view import view
from api.v1.auth_view import auth_view

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

app.config["SECRET_KEY"] = '12345'

app.register_blueprint(view, url_prefix='/view')
app.register_blueprint(auth_view, url_prefix='/auth')

@app.route('/')
def index():
    ''' home '''
    return 'Hello World!'

if __name__ == '__main__':
    with app.app_context():
        app.run()