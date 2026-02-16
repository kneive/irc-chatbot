from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config['JSON_SORT_KEYS'] = False
app.config['DATABASE'] = 'saltmine.db'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)