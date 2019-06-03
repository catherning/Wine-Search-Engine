from flask import Flask
from app.config import ProductionConfig
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
app.config.from_object(ProductionConfig)
run_with_ngrok(app)

from app import routes
