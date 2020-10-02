from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc('do login', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''do login'''
      return newAdvisorlogin(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    pass