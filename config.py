import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
TOKEN = os.getenv("TOKEN")
ORG = os.getenv("ORG")
BUCKET = os.getenv("BUCKET")
NAME = os.getenv('NAME')
