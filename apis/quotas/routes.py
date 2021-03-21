from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list quotas")
    @api.marshal_list_with(model)
    def get(self):
      '''list quotas'''
      return listQuotas()
    @api.doc('find quotas')
    #@api.expect(model)
    #@api.marshal_list_with(model)
    def put(self):
      '''find quotas'''
      return findQuota(api.payload)
    @api.doc('create quota', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create quota'''
      return newQuota(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('edit quota', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''edit quota'''
      return updateQuota(id, api.payload)
    @api.doc('delete quota')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete quota'''
      return deleteQuota(id)
    pass
