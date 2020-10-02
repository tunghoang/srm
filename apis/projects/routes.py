from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list projects")
    @api.marshal_list_with(model)
    def get(self):
      '''list projects'''
      return listProjects()
    @api.doc('find projects')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find projects'''
      return findProject(api.payload)
    @api.doc('create project', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create project'''
      return newProject(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('edit project', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''edit project'''
      return updateProject(id, api.payload)
    @api.doc('delete project')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete project'''
      return deleteProject(id)
    pass