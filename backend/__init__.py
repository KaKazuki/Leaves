import requests
from flask import Flask, render_template
from flask_cors import CORS

from backend.api import api

app = Flask("Leaves-web",
            static_folder='./web/static',
            template_folder='./web')
app.config.from_object('backend.config.ProductionConfig')

app.register_blueprint(api, url_prefix="/api")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
