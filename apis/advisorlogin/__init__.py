from .model import create_model
from .routes import init_routes
from .db import Advisorlogin
from flask_restplus import Namespace

def create_api():
  api = Namespace('advisorlogin', description="login for advisor")
  model = create_model(api)
  init_routes(api, model)
  return api