from .model import create_model
from .routes import init_routes
from .db import Attachment
from flask_restplus import Namespace

def create_api():
  api = Namespace('attachments', description="attachments namespace (bao cao, presentation, source code, ...)")
  model = create_model(api)
  init_routes(api, model)
  return api