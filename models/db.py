from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongodb_password = os.getenv("MONGODB_PASSWORD")
mongodb_name = os.getenv("MONGODB_NAME")

uri = f"mongodb+srv://isefshondo:{mongodb_password}@boecluster.bz4yg1l.mongodb.net/{mongodb_name}?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client[f"{mongodb_name}"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)