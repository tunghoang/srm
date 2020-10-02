from .model import create_model
from .routes import init_routes
from .db import Projectadvisorrel
from flask_restplus import Namespace

def create_api():
  api = Namespace('projectAdvisorRels', description="project-Advisor Relationship")
  model = create_model(api)
  init_routes(api, model)
  return api