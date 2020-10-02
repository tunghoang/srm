from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Projectadvisorrel(__db.Base):
  __tablename__ = "projectAdvisorRel"
  idProjectAdvisorRel = Column(Integer, primary_key = True)
  idAdvisor = Column(Integer, ForeignKey('advisor.idAdvisor'))
  idProject = Column(Integer, ForeignKey('project.idProject'))
  status = Column(Integer)

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idProjectAdvisorRel" in dictModel) and (dictModel["idProjectAdvisorRel"] != None):
      self.idProjectAdvisorRel = dictModel["idProjectAdvisorRel"]
    if ("idAdvisor" in dictModel) and (dictModel["idAdvisor"] != None):
      self.idAdvisor = dictModel["idAdvisor"]
    if ("idProject" in dictModel) and (dictModel["idProject"] != None):
      self.idProject = dictModel["idProject"]
    if ("status" in dictModel) and (dictModel["status"] != None):
      self.status = dictModel["status"]

  def __repr__(self):
    return '<Projectadvisorrel idProjectAdvisorRel={} idAdvisor={} idProject={} status={} >'.format(self.idProjectAdvisorRel, self.idAdvisor, self.idProject, self.status, )

  def json(self):
    return {
      "idProjectAdvisorRel":self.idProjectAdvisorRel,"idAdvisor":self.idAdvisor,"idProject":self.idProject,"status":self.status,
    }

  def update(self, dictModel):
    if ("idProjectAdvisorRel" in dictModel) and (dictModel["idProjectAdvisorRel"] != None):
      self.idProjectAdvisorRel = dictModel["idProjectAdvisorRel"]
    if ("idAdvisor" in dictModel) and (dictModel["idAdvisor"] != None):
      self.idAdvisor = dictModel["idAdvisor"]
    if ("idProject" in dictModel) and (dictModel["idProject"] != None):
      self.idProject = dictModel["idProject"]
    if ("status" in dictModel) and (dictModel["status"] != None):
      self.status = dictModel["status"]

def __recover():
  __db.newSession()

def __doList():
  return __db.session().query(Projectadvisorrel).all()
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Projectadvisorrel).filter(Projectadvisorrel.idProjectadvisorrel == id).scalar()
  doLog("__doGet: {}".format(instance))
  return instance

def __doUpdate(id, model):
  instance = getProjectadvisorrel(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getProjectadvisorrel(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Projectadvisorrel).filter_by(**model).all()
  return results


def listProjectadvisorrels():
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

def newProjectadvisorrel(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Projectadvisorrel(model)
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

def getProjectadvisorrel(id):
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

def updateProjectadvisorrel(id, model):
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

def deleteProjectadvisorrel(id):
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

def findProjectadvisorrel(model):
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