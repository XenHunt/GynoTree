from flask import Flask
from flask_cors import CORS
from config import configuration
from orm import db
from sqlalchemy import text
import os

app = Flask("Family Tree Backend")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{configuration['DB']['USER']}:{configuration['DB']['PASSWORD']}@{configuration['DB']['HOST']}:{configuration['DB']['PORT']}/{configuration['DB']['NAME']}"
)

db.init_app(app)
CORS(app)

with app.app_context():

    if configuration["DEBUG"]:
        with db.engine.connect() as cn:
            with open(os.path.join(os.curdir, "delete.sql"), "r") as f:
                sql = f.read()
                cn.execute(text(sql))
                cn.commit()

    db.create_all()
    if configuration["DEBUG"]:
        with db.engine.connect() as cn:
            with open(os.path.join(os.curdir, "template.sql"), "r") as f:
                sql = f.read()
                cn.execute(text(sql))
                cn.commit()
            
