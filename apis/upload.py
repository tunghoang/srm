from flask import request
from flask_restplus import Namespace, Resource, reqparse
from werkzeug import datastructures
from werkzeug.exceptions import *
from .app_utils import *
import os 
import calendar;
import time;
from datetime import datetime
from .db_utils import *

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

attachmentUploadParser = reqparse.RequestParser()
attachmentUploadParser.add_argument(
  'idProject', type = 'int', location='form', required=True, help = 'project id'
)
attachmentUploadParser.add_argument(
  'idStudent', type = 'int', location='form', required=True, help = 'student id'
)
attachmentUploadParser.add_argument(
  'attach_file', type = datastructures.FileStorage, location='files', required=True, help = 'attachment'
)

try:
  __db = DbInstance()
except Exception as e:
  print(str(e))
def findSemesterId(idProject):
  results = __db.session().execute('SELECT idSemester FROM project WHERE idProject=:idProject', {'idProject': idProject}).fetchall()
  __db.session().commit()
  return results[0][0]

def processAttachment(idProject, idStudent, dataFile, destination, filename):
  destPath = os.path.join(destination, filename)
  params = {
    'title': filename,
    'uuid': destPath,
    'idProject': idProject,
    'idOwner': idStudent,
    'uploadDate': datetime.now()
  }

  os.replace(dataFile, destPath)
  try:
    __db.session().execute("""
      INSERT INTO attachment(title, uuid, idProject, idOwner, uploadDate) 
      VALUES(:title, :uuid, :idProject, :idOwner, :uploadDate)
    """, params)
  except Exception as e:
    print(str(e))
    __db.session().rollback()
    results = __db.session().execute("SELECT uuid FROM attachment WHERE idProject=:idProject AND idOwner=:idOwner", params).fetchall()
    if len(results) > 0:
      os.remove(results[0][0])
      __db.session().execute("""
        UPDATE attachment SET title=:title, uuid=:uuid, uploadDate=:uploadDate 
        WHERE idProject=:idProject AND idOwner=:idOwner
      """, params)
    __db.session().commit()

@uploadApi.route('/attachment')
class AttachmentUploader(Resource):
  @uploadApi.doc("upload attachment")
  @uploadApi.expect(attachmentUploadParser)
  def post(self):
    try: 
      doLog("Attachment upload process")
      doLog(request.files)
      args = attachmentUploadParser.parse_args()
      doLog(args['attach_file'])
      idSemester = findSemesterId(args['idProject'])
      destination = os.path.join(config.get('Default', 'attachment_path', fallback='attachments'), str(idSemester))
      if not os.path.exists(destination):
        os.makedirs(destination)
      filename = os.path.join(destination, args['attach_file'].filename)
      doLog(filename)
      processAttachment(args['idProject'], args['idStudent'], args['attach_file'].stream, destination, args['attach_file'].filename)
    except Exception as e:
      print(str(e))
    return {"status": "success"}

@uploadApi.route('/attachment/<int:id>')
class AttachmentManager(Resource):
  @uploadApi.doc("delete attachment")
  def delete(self, id):
    try:
      params = {'idAttachment': id}
      results = __db.session().execute("SELECT uuid FROM attachment WHERE idAttachment = :idAttachment", params).fetchall()
      if len(results) > 0:
        os.remove(results[0][0])
        __db.session().execute("DELETE FROM attachment WHERE idAttachment = :idAttachment", params)
        __db.session().commit()
    except Exception as e:
      print(str(e))
      __db.session().rollback()

