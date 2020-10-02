from .model import create_model
from .routes import init_routes
from .db import Project
from flask_restplus import Namespace

def create_api():
  api = Namespace('projects', description="projects namespace")
  model = create_model(api)
  init_routes(api, model)
  return api