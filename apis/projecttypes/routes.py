from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list projecttypes")
    @api.marshal_list_with(model)
    def get(self):
      '''list projecttypes'''
      return listProjecttypes()
    @api.doc('find projecttypes')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find projecttypes'''
      return findProjecttype(api.payload)
    @api.doc('create projecttype', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create projecttype'''
      return newProjecttype(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('edit projecttype', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''edit projecttype'''
      return updateProjecttype(id, api.payload)
    @api.doc('delete projecttype')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete projecttype'''
      return deleteProjecttype(id)
    pass