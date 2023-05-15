from flask import Flask
from dotenv import load_dotenv
from controllers.routes import routes

import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)