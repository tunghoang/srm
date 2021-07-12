from flask import request, send_file, session
from flask_restplus import Namespace, Resource
from werkzeug import datastructures
from werkzeug.exceptions import *
from .app_utils import *
from .mail_utils import *
from .emaildata_utils import *
import os 
import traceback
import calendar;
import time;
from .sec_utils import *
from .configs.db import findConfig

emailDataApi = Namespace('emaildata', 'fetch email data for bulk emailing')
@emailDataApi.route('/<string:mode>')
class EmailData(Resource):
  @emailDataApi.doc('fetch email data for bulk emailing')
  def get(self, mode):
    try:
      return send_file(f'public/{mode}.json')
    except Exception as e:
      doLog(e, True)
      raise BadRequest(str(e))

@emailDataApi.route('/templates')
class EmailDataTemplates(Resource):
  @emailDataApi.doc('Get list of email templates')
  def get(self):
    try:
      files = [f for f in os.listdir('public/email-templates/') if os.path.isfile(f'public/email-templates/{f}')]
      return files
    except Exception as e:
      doLog(e, True)
      raise BadRequest(str(e))

@emailDataApi.route('/templates/<string:templateName>')
class EmailDataTemplateFile(Resource):
  @emailDataApi.doc('Get a template by name')
  def get(self, templateName):
    try:
      #header('Content-Type': 'text/plain')
      return send_file(f'public/email-templates/{templateName}', mimetype='text/plain')
    except Exception as e:
      doLog(e, True)
      raise BadRequest(str(e))

@emailDataApi.route('/upload')
class EmailDataUploader(Resource):
  @emailDataApi.doc("Update email data file specified by <mode>")
  def post(self):
    try:
      payload = request.form.to_dict()
      mode = payload['mode']
      xlsxFile = request.files.get(mode);
      if xlsxFile.mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        process(mode, xlsxFile.stream)
        return {'message': 'success'}
      else:
        raise Error('Wrong mimetype')
    except Exception as e:
      raise BadRequest(e)
