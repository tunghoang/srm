from .model import create_model
from .routes import init_routes
from .db import Logout
from flask_restplus import Namespace

def create_api():
  api = Namespace('logout', description="logout")
  model = create_model(api)
  init_routes(api, model)
  return api