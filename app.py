from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # 同源政策

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db" # 這邊使用 sqlite3
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # 🤔



db = SQLAlchemy(app) 

import routes 

with app.app_context():
    db.create_all()