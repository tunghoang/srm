from .model import create_model
from .routes import init_routes
from .db import Projectreviewerrrel
from flask_restplus import Namespace

def create_api():
  api = Namespace('projectReviewerRels', description="project-Reviewer Relationship")
  model = create_model(api)
  init_routes(api, model)
  return api