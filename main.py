from flask import Flask
from .config import configuration

app = Flask("Family Tree")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{configuration['DB']['USER']}:{configuration['DB']['PASSWORD']}@{configuration['DB']['HOST']}:{configuration['DB']['PORT']}/{configuration['DB']['NAME']}"
)

app.run(debug=configuration["DEBUG"])
