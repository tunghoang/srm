from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list project reviewer rel")
    @api.marshal_list_with(model)
    def get(self):
      '''list project reviewer rels'''
      return listProjectreviewerrrels()
    @api.doc('find projectreviewer rels')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find projectreviewer rels'''
      return findProjectreviewerrrel(api.payload)
    @api.doc('create project reviewer rel', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create project reviewer rel'''
      return newProjectreviewerrrel(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('edit project reviewer rel', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''edit project reviewer rel'''
      return updateProjectreviewerrrel(id, api.payload)
    @api.doc('delete project reviewer rel')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete project reviewer rel'''
      return deleteProjectreviewerrrel(id)
    pass