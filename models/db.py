from pymongo import MongoClient
from dotenv import load_dotenv

import os

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

client = MongoClient(f"mongodb://{db_host}:{db_port}/")
db = client[db_name]

collectionUser = db["usuario"]
collectionRecords = db["historico"]
collectionCattle = db["gado"]