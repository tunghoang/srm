from flask import request,send_from_directory
from flask_restplus import Namespace, Resource, reqparse
from werkzeug import datastructures
from werkzeug.exceptions import *
from .app_utils import *
import os 
import calendar;
import time;
from .db_utils import DbInstance
from .advisors.db import dumpAdvisors

def findActiveSemester() :
  __db = DbInstance.getInstance()
  queryStr = """
    SELECT idSemester FROM semester WHERE semesterIndex = IF(month(curdate()) < 7, 1, 0) AND YEAR(curdate()) = year + semesterIndex
  """
  doLog(queryStr)
  result = __db.session().execute(queryStr, {}).fetchall()
  __db.session().commit()
  if len(result) > 0:
    print(result[0][0])
    return result[0][0]
  else:
    raise BadRequest("Semester not exists")
  

exportAdvisorApi = Namespace('exportAdvisors', "export all advisor to excel")
@exportAdvisorApi.route('/')
class XlsxExportAdvisors(Resource):
  @exportAdvisorApi.doc("Export all advisors to excel file")
  def get(self):
    doLog("Export advisors")
    results = dumpAdvisors()
    df = toDataFrame(results)
    print(df)
    df.to_excel('public/advisors.xlsx', index=False, engine='xlsxwriter')
    return send_from_directory('public', 'advisors.xlsx')

from .studentSemesterRels.db import findStudentsemesterrel
exportStudentSemesterApi = Namespace('exportStudentSemester', 'export all student in semester')
@exportStudentSemesterApi.route('/<int:id>')
class XlsxExportStudentSemester(Resource):
  @exportStudentSemesterApi.doc("Export all students going to graduate in a semester")
  def get(self, id):
    doLog("Export students in a semester " + str(id))
    results = findStudentsemesterrel({'idSemester':id})
    df = toDataFrame(results)
    df.to_excel('public/studentSemester.xlsx', index=False, engine='xlsxwriter')
    return send_from_directory('public', 'studentSemester.xlsx')

recordCheckpointApi = Namespace('checkpoint', 'record checkpoint')
@recordCheckpointApi.route('/')
class CheckpointRecorder(Resource):
  @recordCheckpointApi.doc("Record checkpoint to csv file - begin")
  def get(self):
    try:
      id = findActiveSemester()
      doLog("record checkpoint for semester " + str(id))
      results = findStudentsemesterrel({'idSemester':id})
      df = toDataFrame(results)
      df.to_csv('checkpoints/studentSemester-begin.csv', sep="|")
      return {'msg': "checkpoint recorded"}
    except Exception as e:
      print(str(e))
      raise(e)

  @recordCheckpointApi.doc("Record checkpoint to csv file - end")
  def post(self):
    try:
      id = findActiveSemester()
      doLog("record checkpoint for semester " + str(id))
      results = findStudentsemesterrel({'idSemester':id})
      df = toDataFrame(results)
      df.to_csv('checkpoints/studentSemester-end.csv', sep="|")
      return {'msg': "checkpoint recorded"}
    except Exception as e:
      print(str(e))
      raise(e)
  @recordCheckpointApi.doc("Compare checkpoints")
  def put(self):
    try:
      os.system('diff checkpoints/studentSemester-begin.csv checkpoints/studentSemester-end.csv | grep -E "(>|<)" > public/checkpoint-diff.csv')
      return send_from_directory('public', 'checkpoint-diff.csv')
    except Exception as e:
      print(str(e))
      raise(e)
