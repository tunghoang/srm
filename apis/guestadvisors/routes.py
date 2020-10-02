from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list guest advisors")
    @api.marshal_list_with(model)
    def get(self):
      '''list guest advisors'''
      return listGuestadvisors()
    @api.doc('find guest advisors')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find guest advisors'''
      return findGuestadvisor(api.payload)
    @api.doc('create guest advisor', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create guest advisor'''
      return newGuestadvisor(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('edit guest advisor', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''edit guest advisor'''
      return updateGuestadvisor(id, api.payload)
    @api.doc('delete guest advisor')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete guest advisor'''
      return deleteGuestadvisor(id)
    pass