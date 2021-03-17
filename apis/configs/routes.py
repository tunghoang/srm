from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list global configs")
    @api.marshal_list_with(model)
    def get(self):
      '''list global configs'''
      return listConfigs()
    @api.doc('new global config', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''new global config'''
      return newConfig(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('update global config', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''update global config'''
      return updateConfig(id, api.payload)
    pass