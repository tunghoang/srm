from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list attachments")
    @api.marshal_list_with(model)
    def get(self):
      '''list attachments'''
      return listAttachments()
    @api.doc('find attachments')
    @api.expect(model)
    @api.marshal_list_with(model)
    def put(self):
      '''find attachments'''
      return findAttachment(api.payload)
    @api.doc('create attachment', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create attachment'''
      return newAttachment(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('edit attachment', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''edit attachment'''
      return updateAttachment(id, api.payload)
    @api.doc('delete attachment')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete attachment'''
      return deleteAttachment(id)
    pass