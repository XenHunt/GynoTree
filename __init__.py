from routes import app
from config import configuration

app.run(debug=configuration["DEBUG"])
