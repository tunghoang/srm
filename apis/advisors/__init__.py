from .model import create_model
from .routes import init_routes
from .db import Advisor
from flask_restplus import Namespace

def create_api():
  api = Namespace('advisors', description="advisors namespace")
  model = create_model(api)
  init_routes(api, model)
  return api