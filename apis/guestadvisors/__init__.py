from .model import create_model
from .routes import init_routes
from .db import Guestadvisor
from flask_restplus import Namespace

def create_api():
  api = Namespace('guestadvisors', description="guest advisor namespace")
  model = create_model(api)
  init_routes(api, model)
  return api