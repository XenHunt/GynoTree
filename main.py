from flask import Flask
from flask_cors import CORS
from config import configuration
from orm import db

app = Flask("Family Tree Backend")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{configuration['DB']['USER']}:{configuration['DB']['PASSWORD']}@{configuration['DB']['HOST']}:{configuration['DB']['PORT']}/{configuration['DB']['NAME']}"
)

db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()
