from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Project(__db.Base):
  __tablename__ = "project"
  idProject = Column(Integer, primary_key = True)
  title = Column(Text)
  idProjecttype = Column(Integer, ForeignKey('projecttype.idProjecttype'))
  idSemester = Column(Integer, ForeignKey('semester.idSemester'))
  status = Column(String(20))
  grade = Column(Float)

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idProject" in dictModel) and (dictModel["idProject"] != None):
      self.idProject = dictModel["idProject"]
    if ("title" in dictModel) and (dictModel["title"] != None):
      self.title = dictModel["title"]
    if ("idProjecttype" in dictModel) and (dictModel["idProjecttype"] != None):
      self.idProjecttype = dictModel["idProjecttype"]
    if ("idSemester" in dictModel) and (dictModel["idSemester"] != None):
      self.idSemester = dictModel["idSemester"]
    if ("status" in dictModel) and (dictModel["status"] != None):
      self.status = dictModel["status"]
    if ("grade" in dictModel) and (dictModel["grade"] != None):
      self.grade = dictModel["grade"]

  def __repr__(self):
    return '<Project idProject={} title={} idProjecttype={} idSemester={} status={} grade={} >'.format(self.idProject, self.title, self.idProjecttype, self.idSemester, self.status, self.grade, )

  def json(self):
    return {
      "idProject":self.idProject,"title":self.title,"idProjecttype":self.idProjecttype,"idSemester":self.idSemester,"status":self.status,"grade":self.grade,
    }

  def update(self, dictModel):
    if ("idProject" in dictModel) and (dictModel["idProject"] != None):
      self.idProject = dictModel["idProject"]
    if ("title" in dictModel) and (dictModel["title"] != None):
      self.title = dictModel["title"]
    if ("idProjecttype" in dictModel) and (dictModel["idProjecttype"] != None):
      self.idProjecttype = dictModel["idProjecttype"]
    if ("idSemester" in dictModel) and (dictModel["idSemester"] != None):
      self.idSemester = dictModel["idSemester"]
    if ("status" in dictModel) and (dictModel["status"] != None):
      self.status = dictModel["status"]
    if ("grade" in dictModel) and (dictModel["grade"] != None):
      self.grade = dictModel["grade"]

def __recover():
  __db.newSession()

def __doList():
  return __db.session().query(Project).all()
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Project).filter(Project.idProject == id).scalar()
  doLog("__doGet: {}".format(instance))
  return instance

def __doUpdate(id, model):
  instance = getProject(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getProject(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Project).filter_by(**model).all()
  return results


def listProjects():
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

def newProject(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Project(model)
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

def getProject(id):
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

def updateProject(id, model):
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

def deleteProject(id):
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

def findProject(model):
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