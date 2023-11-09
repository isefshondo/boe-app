from controllers.utils import Cache
from flask import Flask
from flask_cors import CORS
from controllers.Routes import routes

app = Flask(__name__)

CORS(app)

Cache.configurationCache(app)

app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)