from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Projectreviewerrrel(__db.Base):
  __tablename__ = "projectReviewerrRel"
  idProjectreviewerrel = Column(Integer, primary_key = True)
  idReviewer = Column(Integer, ForeignKey('advisor.idAdvisor'))
  idProject = Column(Integer, ForeignKey('project.idProject'))
  status = Column(Integer)

  constraints = list()
  constraints.append(UniqueConstraint('idProject','idReviewer'))
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idProjectreviewerrel" in dictModel) and (dictModel["idProjectreviewerrel"] != None):
      self.idProjectreviewerrel = dictModel["idProjectreviewerrel"]
    if ("idReviewer" in dictModel) and (dictModel["idReviewer"] != None):
      self.idReviewer = dictModel["idReviewer"]
    if ("idProject" in dictModel) and (dictModel["idProject"] != None):
      self.idProject = dictModel["idProject"]
    if ("status" in dictModel) and (dictModel["status"] != None):
      self.status = dictModel["status"]

  def __repr__(self):
    return '<Projectreviewerrrel idProjectreviewerrel={} idReviewer={} idProject={} status={} >'.format(self.idProjectreviewerrel, self.idReviewer, self.idProject, self.status, )

  def json(self):
    return {
      "idProjectreviewerrel":self.idProjectreviewerrel,"idReviewer":self.idReviewer,"idProject":self.idProject,"status":self.status,
    }

  def update(self, dictModel):
    if ("idProjectreviewerrel" in dictModel) and (dictModel["idProjectreviewerrel"] != None):
      self.idProjectreviewerrel = dictModel["idProjectreviewerrel"]
    if ("idReviewer" in dictModel) and (dictModel["idReviewer"] != None):
      self.idReviewer = dictModel["idReviewer"]
    if ("idProject" in dictModel) and (dictModel["idProject"] != None):
      self.idProject = dictModel["idProject"]
    if ("status" in dictModel) and (dictModel["status"] != None):
      self.status = dictModel["status"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Projectreviewerrrel).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Projectreviewerrrel).filter(Projectreviewerrrel.idProjectreviewerrrel == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getProjectreviewerrrel(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getProjectreviewerrrel(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Projectreviewerrrel).filter_by(**model).all()
  __db.session().commit()
  return results


def listProjectreviewerrrels():
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

def newProjectreviewerrrel(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Projectreviewerrrel(model)
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

def getProjectreviewerrrel(id):
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

def updateProjectreviewerrrel(id, model):
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

def deleteProjectreviewerrrel(id):
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

def findProjectreviewerrrel(model):
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