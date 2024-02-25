#!/usr/bin/python3
""""
Creating a flask blueprint
"""
from flask import Blueprint
from api.v1.views.index import *


app_views = Blueprint("/api/v1")
