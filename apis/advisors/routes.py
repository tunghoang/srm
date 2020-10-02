from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list advisors")
    @api.marshal_list_with(model)
    def get(self):
      '''list advisors'''
      return listAdvisors()
    @api.doc('find advisors')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find advisors'''
      return findAdvisor(api.payload)
    @api.doc('create advisor', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create advisor'''
      return newAdvisor(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('edit advisor', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''edit advisor'''
      return updateAdvisor(id, api.payload)
    @api.doc('delete advisor')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete advisor'''
      return deleteAdvisor(id)
    pass