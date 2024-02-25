#!/usr/bin/python3
"""
Creating routes
"""
from api.v1.views import app_views
from flask import jsonify


@app.route("/status")
def status_ok():
    return (jsonify({"status": "OK"}))
