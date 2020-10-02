from .model import create_model
from .routes import init_routes
from .db import Projecttype
from flask_restplus import Namespace

def create_api():
  api = Namespace('projecttypes', description="project types (KLTN, Du an, NCKH)")
  model = create_model(api)
  init_routes(api, model)
  return api