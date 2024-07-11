import os

API_KEY = os.environ.get("API_KEY") # TODO: local build logic

def auth(key):
    return key == API_KEY
