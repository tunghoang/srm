from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list students")
    @api.marshal_list_with(model)
    def get(self):
      '''list students'''
      return listStudents()
    @api.doc('find students')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find students'''
      return findStudent(api.payload)
    @api.doc('create student', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create student'''
      return newStudent(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('edit student', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''edit student'''
      return updateStudent(id, api.payload)
    @api.doc('delete student')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete student'''
      return deleteStudent(id)
    pass