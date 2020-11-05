from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list project student rel")
    @api.marshal_list_with(model)
    def get(self):
      '''list project student rels'''
      return listProjectstudentrels()
    @api.doc('find projectstudent rels')
    @api.expect(model)
    #@api.marshal_list_with(model)
    def put(self):
      '''find projectstudent rels'''
      return findProjectstudentrel(api.payload)
    @api.doc('create project student rel', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create project student rel'''
      return newProjectstudentrel(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('edit project student rel', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''edit project student rel'''
      return updateProjectstudentrel(id, api.payload)
    @api.doc('delete project student rel')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete project student rel'''
      return deleteProjectstudentrel(id)
    pass
