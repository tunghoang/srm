from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list classes")
    @api.marshal_list_with(model)
    def get(self):
      '''list classes'''
      return listKlasss()
    @api.doc('find class')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find class'''
      return findKlass(api.payload)
    @api.doc('create class', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create class'''
      return newKlass(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('edit class', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''edit class'''
      return updateKlass(id, api.payload)
    @api.doc('delete class')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete class'''
      return deleteKlass(id)
    pass