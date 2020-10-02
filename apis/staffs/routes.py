from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list staffs")
    @api.marshal_list_with(model)
    def get(self):
      '''list staffs'''
      return listStaffs()
    @api.doc('find staffs')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find staffs'''
      return findStaff(api.payload)
    @api.doc('create staff', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create staff'''
      return newStaff(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('edit staff', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''edit staff'''
      return updateStaff(id, api.payload)
    @api.doc('delete staff')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete staff'''
      return deleteStaff(id)
    pass