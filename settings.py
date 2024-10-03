import datetime
from flask import Flask

class Config:
    DEBUG = True
    TESTING = True
    SECRET_KEY = '__secret_key'

host = "127.0.0.1"
app = Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)

user = "postgres"
password = "12345"
db_name = "food_helper"


app.config.from_object(Config)