from .model import create_model
from .routes import init_routes
from .db import Quota
from flask_restplus import Namespace

def create_api():
  api = Namespace('quotas', description="quotas namespace (quotas for bachelor, master, phD, PGS, ...)")
  model = create_model(api)
  init_routes(api, model)
  return api