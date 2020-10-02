from .model import create_model
from .routes import init_routes
from .db import Projectstudentrel
from flask_restplus import Namespace

def create_api():
  api = Namespace('projectStudentRels', description="project-Student Relationship")
  model = create_model(api)
  init_routes(api, model)
  return api