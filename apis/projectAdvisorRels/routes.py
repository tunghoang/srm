from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list project advisor rel")
    @api.marshal_list_with(model)
    def get(self):
      '''list project advisor rels'''
      return listProjectadvisorrels()
    @api.doc('find projectadvisor rels')
    @api.expect(model)
    #@api.marshal_list_with(model)
    def put(self):
      '''find projectadvisor rels'''
      return findProjectadvisorrel(api.payload)
    @api.doc('create project advisor rel', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create project advisor rel'''
      return newProjectadvisorrel(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('edit project advisor rel', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''edit project advisor rel'''
      return updateProjectadvisorrel(id, api.payload)
    @api.doc('delete project advisor rel')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete project advisor rel'''
      return deleteProjectadvisorrel(id)
    pass
