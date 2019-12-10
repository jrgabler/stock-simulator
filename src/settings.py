import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
TRADIER_API_KEY = os.environ.get("TRADIER_API_KEY")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
