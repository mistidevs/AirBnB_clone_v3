#!/usr/bin/python3
"""
Creating a variable of instance Flask
"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    """Closing storage to refresh instance"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Handling 404 requests """
    response = {"error": "Not found"}
    return make_response(jsonify(response), 404)


if __name__ == '__main__':
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 500))
    app.run(host=host, port=port, threaded=True)
