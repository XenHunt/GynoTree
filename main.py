from flask import Flask
from .config import configuration

app = Flask("Family Tree")


app.run(debug=configuration["DEBUG"])
