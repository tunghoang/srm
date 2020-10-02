from .model import create_model
from .routes import init_routes
from .db import Studentlogin
from flask_restplus import Namespace

def create_api():
  api = Namespace('studentlogin', description="login for student")
  model = create_model(api)
  init_routes(api, model)
  return api