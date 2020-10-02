from .model import create_model
from .routes import init_routes
from .db import Guestlogin
from flask_restplus import Namespace

def create_api():
  api = Namespace('guestlogin', description="login for guest")
  model = create_model(api)
  init_routes(api, model)
  return api