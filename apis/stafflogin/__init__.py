from .model import create_model
from .routes import init_routes
from .db import Stafflogin
from flask_restplus import Namespace

def create_api():
  api = Namespace('stafflogin', description="login for staff")
  model = create_model(api)
  init_routes(api, model)
  return api