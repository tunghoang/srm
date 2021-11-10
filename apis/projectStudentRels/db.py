from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

from ..students import Student

from ..sec_utils import *
__db = DbInstance.getInstance()

class Projectstudentrel(__db.Base):
  __tablename__ = "projectStudentRel"
  idProjectstudentrel = Column(Integer, primary_key = True)
  idStudent = Column(Integer, ForeignKey('student.idStudent'), nullable=False)
  idProject = Column(Integer, ForeignKey('project.idProject'), nullable=False)
  status = Column(Integer)

  constraints = list()
  constraints.append(UniqueConstraint('idProject','idStudent'))
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idProjectstudentrel" in dictModel) and (dictModel["idProjectstudentrel"] != None):
      self.idProjectstudentrel = dictModel["idProjectstudentrel"]
    if ("idStudent" in dictModel) and (dictModel["idStudent"] != None):
      self.idStudent = dictModel["idStudent"]
    if ("idProject" in dictModel) and (dictModel["idProject"] != None):
      self.idProject = dictModel["idProject"]
    if ("status" in dictModel) and (dictModel["status"] != None):
      self.status = dictModel["status"]

  def __repr__(self):
    return '<Projectstudentrel idProjectstudentrel={} idStudent={} idProject={} status={} >'.format(self.idProjectstudentrel, self.idStudent, self.idProject, self.status, )

  def json(self):
    return {
      "idProjectstudentrel":self.idProjectstudentrel,"idStudent":self.idStudent,"idProject":self.idProject,"status":self.status,
    }

  def update(self, dictModel):
    if ("idProjectstudentrel" in dictModel) and (dictModel["idProjectstudentrel"] != None):
      self.idProjectstudentrel = dictModel["idProjectstudentrel"]
    if ("idStudent" in dictModel) and (dictModel["idStudent"] != None):
      self.idStudent = dictModel["idStudent"]
    if ("idProject" in dictModel) and (dictModel["idProject"] != None):
      self.idProject = dictModel["idProject"]
    if ("status" in dictModel) and (dictModel["status"] != None):
      self.status = dictModel["status"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Projectstudentrel).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Projectstudentrel).filter(Projectstudentrel.idProjectstudentrel == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getProjectstudentrel(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getProjectstudentrel(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  queryObj = __db.session().query(Student.fullname, Student.studentNumber, Projectstudentrel.idStudent, Projectstudentrel.idProject, Projectstudentrel.idProjectstudentrel).filter(Student.idStudent == Projectstudentrel.idStudent)
  if 'idProject' in model:
    queryObj = queryObj.filter(Projectstudentrel.idProject == model['idProject'])
  if 'idStudent' in model:
    queryObj = queryObj.filter(Projectstudentrel.idStudent == model['idStudent'])
  if 'status' in model:
    queryObj = queryObj.filter(Projectstudentrel.status == model['status'])

  results = queryObj.all()

  __db.session().commit()
  return list(map(lambda x:{'fullname':x[0], 'studentNumber':x[1], 'idStudent':x[2], 'idProject':x[3], 'idProjectstudentrel': x[4]}, results))


def listProjectstudentrels():
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

def newProjectstudentrel(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Projectstudentrel(model)
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

def getProjectstudentrel(id):
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

def updateProjectstudentrel(id, model):
  instance = getProjectstudentrel(id)
  verifyIdStudent(request, session, instance.json())
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

def deleteProjectstudentrel(id):
  instance = getProjectstudentrel(id)
  verifyIdStudent(request, session, instance.json())
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

def findProjectstudentrel(model):
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
