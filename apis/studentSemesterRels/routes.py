from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list student semester relationships")
    @api.marshal_list_with(model)
    def get(self):
      '''list student semester relationships'''
      return listStudentsemesterrels()
    @api.doc('find student semester rels')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find student semester rels'''
      return findStudentsemesterrel(api.payload)
    @api.doc('create student semester relationship', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create student semester relationship'''
      return newStudentsemesterrel(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('update student semester relationship', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''update student semester relationship'''
      return updateStudentsemesterrel(id, api.payload)
    @api.doc('delete student semester relationship')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete student semester relationship'''
      return deleteStudentsemesterrel(id)
    pass