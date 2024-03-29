import traceback
from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Semester(__db.Base):
  __tablename__ = "semester"
  idSemester = Column(Integer, primary_key = True)
  year = Column(Integer)
  semesterIndex = Column(Integer)
  active = Column(Boolean)

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idSemester" in dictModel) and (dictModel["idSemester"] != None):
      self.idSemester = dictModel["idSemester"]
    if ("year" in dictModel) and (dictModel["year"] != None):
      self.year = dictModel["year"]
    if ("semesterIndex" in dictModel) and (dictModel["semesterIndex"] != None):
      self.semesterIndex = dictModel["semesterIndex"]
    if ("active" in dictModel) and (dictModel["active"] != None):
      self.active = dictModel["active"]

  def __repr__(self):
    return '<Semester idSemester={} year={} semesterIndex={} active={} >'.format(self.idSemester, self.year, self.semesterIndex, self.active, )

  def json(self):
    return {
      "idSemester":self.idSemester,"year":self.year,"semesterIndex":self.semesterIndex,"active":self.active,
    }

  def update(self, dictModel):
    if ("idSemester" in dictModel) and (dictModel["idSemester"] != None):
      self.idSemester = dictModel["idSemester"]
    if ("year" in dictModel) and (dictModel["year"] != None):
      self.year = dictModel["year"]
    if ("semesterIndex" in dictModel) and (dictModel["semesterIndex"] != None):
      self.semesterIndex = dictModel["semesterIndex"]
    if ("active" in dictModel) and (dictModel["active"] != None):
      self.active = dictModel["active"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Semester).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Semester).filter(Semester.idSemester == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getSemester(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getSemester(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Semester).filter_by(**model).all()
  __db.session().commit()
  return results


def listSemesters():
  doLog("list DAO function")
  try:
    return __doList()
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doList()
  except InterfaceError as e:
    doLog(e)
    __recover()
    return __doList()
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def newSemester(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Semester(model)
  res = False
  try:
    return __doNew(instance)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doNew(instance)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def getSemester(id):
  doLog("get DAO function", id)
  try:
    return __doGet(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doGet(id)
  except InterfaceError as e:
    doLog(e)
    __recover()
    return __doGet(id)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def updateSemester(id, model):
  doLog("update DAO function. Model: {}".format(model))
  try:
    return __doUpdate(id, model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doUpdate(id, model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def deleteSemester(id):
  doLog("delete DAO function", id)
  try:
    return __doDelete(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doDelete(id)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def findSemester(model):
  doLog("find DAO function %s" % model)
  try:
    return __doFind(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doFind(model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def completeSemester(idSemester):
  sql = '''
  update project set status="finished" where idProject in (
    SELECT distinct att.idProject 
    FROM attachment att
      INNER JOIN projectStudentRel psr ON att.idProject = psr.idProject
      INNER JOIN studentSemesterRel ssr ON psr.idStudent = ssr.idStudent
      INNER JOIN projectAdvisorRel par ON att.idProject = par.idProject
    WHERE ssr.idSemester = :idSemester 
      AND par.status > 0
      AND att.advisorApproved is TRUE
  )
'''
  try:
    __db.session().execute(sql, {'idSemester': idSemester})
    __db.session().commit()
    return {'message': 'Success'}
  except Exception as e:
    traceback.print_exc()
    __db.session().rollback()
    raise BadRequest(e)
