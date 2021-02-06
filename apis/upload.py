from flask import request
from flask_restplus import Namespace, Resource, reqparse
from werkzeug import datastructures
from werkzeug.exceptions import *
from .app_utils import *
import os 
import calendar;
import time;
from .db_utils import config

parser = reqparse.RequestParser()
parser.add_argument(
  'xlsx_file',
  type=datastructures.FileStorage,
  location='files',
  required=True,
  help='XLSX file'
)

uploadApi = Namespace('upload', "upload list of student for each semester")
@uploadApi.route('/studentSemesterXlsx')
class StudentSemesterXlsx(Resource):
  @uploadApi.doc("upload student semester excel file")
  @uploadApi.expect(parser)
  def post(self):
    doLog("Process")
    doLog(request.files)
    args = parser.parse_args()
    doLog(args['xlsx_file'])
    if args['xlsx_file'].mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
      destination = config.get('Default','data_path', fallback='/tmp/')
      if not os.path.exists(destination):
        os.makedirs(destination)
      
      #ts = calendar.timegm(time.gmtime())
      filename = destination + args['xlsx_file'].filename
      doLog(args['xlsx_file'])
      doLog(filename)
      processStudentListUpload(args['xlsx_file'].stream, doLog)
      #args['xlsx_file'].save(filename)
    else:
      raise BadRequest("Request is malformed")
    return {"status": "success"}
