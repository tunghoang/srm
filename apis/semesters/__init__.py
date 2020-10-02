from .model import create_model
from .routes import init_routes
from .db import Semester
from flask_restplus import Namespace

def create_api():
  api = Namespace('semesters', description="semesters namespace (hoc ky)")
  model = create_model(api)
  init_routes(api, model)
  return api