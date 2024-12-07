from flask import Flask
from config import configuration
from orm import db

app = Flask("Family Tree")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{configuration['DB']['USER']}:{configuration['DB']['PASSWORD']}@{configuration['DB']['HOST']}:{configuration['DB']['PORT']}/{configuration['DB']['NAME']}"
)

db.init_app(app)

with app.app_context():
    db.create_all()
