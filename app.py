from controllers.utils import Cache
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from controllers.Routes import routes

import os

load_dotenv()

app = Flask(__name__)

CORS(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Cache.configurationCache(app)

app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)