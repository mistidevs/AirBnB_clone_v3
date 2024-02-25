#!/usr/bin/python3
"""
Creating routes
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=["GET"])
def status_ok():
    """Yields OK"""
    return (jsonify({
        "status": "OK"
    }))
