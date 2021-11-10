from flask import request,send_from_directory
from flask_restplus import Namespace, Resource, reqparse
from werkzeug import datastructures
from werkzeug.exceptions import *
from .app_utils import *
import os 
import calendar;
import time;
import traceback
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

def findProject(idSemester):
  __db = DbInstance.getInstance()
  queryStr = """
    SELECT prj.idProject, prj.title, stu.fullname, stu.studentNumber
    FROM project prj 
      INNER JOIN projectStudentRel psr
        ON prj.idProject = psr.idProject
      INNER JOIN student stu
        ON psr.idStudent = stu.idStudent
    WHERE idSemester = :idSemester
    ORDER BY prj.idProject
  """
  doLog(queryStr)
  result = __db.session().execute(queryStr, {'idSemester': idSemester}).fetchall()
  __db.session().commit()
  return result  

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
@recordCheckpointApi.route('/<int:id>')
class CheckpointRecorder(Resource):
  @recordCheckpointApi.doc("Record checkpoint to csv file - begin")
  def get(self, id):
    try:
      doLog("record checkpoint for semester " + str(id))
      results = findProject(id)
      df = toDataFrame(results)
      df.to_csv(f'checkpoints/studentSemester-{id}-begin.csv', sep="|")
      return {'msg': "checkpoint recorded"}
    except Exception as e:
      print(str(e))
      traceback.print_exc()
      raise(e)

  @recordCheckpointApi.doc("Record checkpoint to csv file - end")
  def post(self, id):
    try:
      doLog("record checkpoint for semester " + str(id))
      results = findProject(id)
      df = toDataFrame(results)
      df.to_csv(f'checkpoints/studentSemester-{id}-end.csv', sep="|")
      return {'msg': "checkpoint recorded"}
    except Exception as e:
      print(str(e))
      traceback.print_exc()
      raise(e)
  @recordCheckpointApi.doc("Compare checkpoints")
  def put(self, id):
    try:
      doLog("Compare checkpoint for semester " + str(id))
      os.system(f'diff checkpoints/studentSemester-{id}-begin.csv checkpoints/studentSemester-{id}-end.csv | grep -E "(>|<)" > public/checkpoint-{id}-diff.csv')
      doLog("diff is done")
      return send_from_directory('public', f'checkpoint-{id}-diff.csv')
    except Exception as e:
      print(str(e))
      traceback.print_exc()
      raise(e)
