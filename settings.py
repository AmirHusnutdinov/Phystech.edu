import datetime
from flask import Flask

host = "127.0.0.1"

app = Flask(__name__)
app.config["SECRET_KEY"] = "__secret_key"
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)

user = "postgres"
password = "12345"
db_name = "phystech"
