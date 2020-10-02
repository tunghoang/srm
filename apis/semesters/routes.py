from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list semesters")
    @api.marshal_list_with(model)
    def get(self):
      '''list semesters'''
      return listSemesters()
    @api.doc('find semesters')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find semesters'''
      return findSemester(api.payload)
    @api.doc('create semester', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create semester'''
      return newSemester(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('edit semester', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''edit semester'''
      return updateSemester(id, api.payload)
    @api.doc('delete semester')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete semester'''
      return deleteSemester(id)
    pass