from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("do logout")
    @api.marshal_list_with(model)
    def get(self):
      '''do login'''
      return listLogouts()

  @api.route('/<int:id>')
  class Instance(Resource):
    pass