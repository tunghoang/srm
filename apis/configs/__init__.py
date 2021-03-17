from .model import create_model
from .routes import init_routes
from .db import Config
from flask_restplus import Namespace

def create_api():
  api = Namespace('configs', description="configs")
  model = create_model(api)
  init_routes(api, model)
  return api