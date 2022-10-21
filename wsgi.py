from dotenv import load_dotenv
from os import path
if path.exists('.env'):
    load_dotenv('.env')
if path.exists('.flaskenv'):
    load_dotenv('.flaskenv')
from co2 import create_app
app = create_app('production')
