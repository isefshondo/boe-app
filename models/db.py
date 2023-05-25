from pymongo import MongoClient
from dotenv import load_dotenv

import os

load_dotenv()

# client = MongoClient('mongodb://localhost:27017')

# db = client['boe-app']

db_host = os.getenv("DB_HOST")
db_password = os.getenv("DB_PASSWORD")

client = MongoClient("mongodb+srv://" + db_host + ":" + db_password + "@cluster0.oxt2a9r.mongodb.net/?retryWrites=true&w=majority")

db = client["boe"]