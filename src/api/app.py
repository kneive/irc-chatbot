from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__) # __name__ specifies where to look for resources

CORS(app)

app.config['JSON_SORT_KEYS']

