from os import getenv
from flask import Flask

app = Flask("Family Tree")


app.run(debug=bool(getenv("DEBUG")))
