from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Studentsemesterrel(__db.Base):
  __tablename__ = "studentSemesterRel"
  idStudentsemesterrel = Column(Integer, primary_key = True)
  idSemester = Column(Integer, ForeignKey('semester.idSemester'))
  idStudent = Column(Integer, ForeignKey('student.idStudent'))
  removed = Column(Integer)

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idStudentsemesterrel" in dictModel) and (dictModel["idStudentsemesterrel"] != None):
      self.idStudentsemesterrel = dictModel["idStudentsemesterrel"]
    if ("idSemester" in dictModel) and (dictModel["idSemester"] != None):
      self.idSemester = dictModel["idSemester"]
    if ("idStudent" in dictModel) and (dictModel["idStudent"] != None):
      self.idStudent = dictModel["idStudent"]
    if ("removed" in dictModel) and (dictModel["removed"] != None):
      self.removed = dictModel["removed"]

  def __repr__(self):
    return '<Studentsemesterrel idStudentsemesterrel={} idSemester={} idStudent={} removed={} >'.format(self.idStudentsemesterrel, self.idSemester, self.idStudent, self.removed, )

  def json(self):
    return {
      "idStudentsemesterrel":self.idStudentsemesterrel,"idSemester":self.idSemester,"idStudent":self.idStudent,"removed":self.removed,
    }

  def update(self, dictModel):
    if ("idStudentsemesterrel" in dictModel) and (dictModel["idStudentsemesterrel"] != None):
      self.idStudentsemesterrel = dictModel["idStudentsemesterrel"]
    if ("idSemester" in dictModel) and (dictModel["idSemester"] != None):
      self.idSemester = dictModel["idSemester"]
    if ("idStudent" in dictModel) and (dictModel["idStudent"] != None):
      self.idStudent = dictModel["idStudent"]
    if ("removed" in dictModel) and (dictModel["removed"] != None):
      self.removed = dictModel["removed"]

def __recover():
  __db.newSession()

def __doList():
  return __db.session().query(Studentsemesterrel).all()
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Studentsemesterrel).filter(Studentsemesterrel.idStudentsemesterrel == id).scalar()
  doLog("__doGet: {}".format(instance))
  return instance

def __doUpdate(id, model):
  instance = getStudentsemesterrel(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getStudentsemesterrel(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Studentsemesterrel).filter_by(**model).all()
  return results


def listStudentsemesterrels():
  doLog("list DAO function")
  try:
    return __doList()
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doList()
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def newStudentsemesterrel(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Studentsemesterrel(model)
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

def getStudentsemesterrel(id):
  doLog("get DAO function", id)
  try:
    return __doGet(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doGet(id)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def updateStudentsemesterrel(id, model):
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

def deleteStudentsemesterrel(id):
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

def findStudentsemesterrel(model):
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