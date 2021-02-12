from flask import request,send_from_directory
from flask_restplus import Namespace, Resource, reqparse
from werkzeug import datastructures
from werkzeug.exceptions import *
from .app_utils import *
import os 
import calendar;
import time;
from .db_utils import config
from .advisors.db import dumpAdvisors

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
