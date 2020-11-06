from .model import create_model
from .routes import init_routes
from .db import Studentsemesterrel
from flask_restplus import Namespace

def create_api():
  api = Namespace('studentSemesterRels', description="student semester relationship")
  model = create_model(api)
  init_routes(api, model)
  return api