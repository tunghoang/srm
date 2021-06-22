from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Attachment(__db.Base):
  __tablename__ = "attachment"
  idAttachment = Column(Integer, primary_key = True)
  title = Column(String(255))
  uuid = Column(String(512))
  idProject = Column(Integer, ForeignKey('project.idProject'))
  idOwner = Column(Integer, ForeignKey('student.idStudent'))
  advisorApproved = Column(Boolean)
  uploadDate = Column(DateTime)

  constraints = list()
  constraints.append(UniqueConstraint('idProject','idOwner'))
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idAttachment" in dictModel) and (dictModel["idAttachment"] != None):
      self.idAttachment = dictModel["idAttachment"]
    if ("title" in dictModel) and (dictModel["title"] != None):
      self.title = dictModel["title"]
    if ("uuid" in dictModel) and (dictModel["uuid"] != None):
      self.uuid = dictModel["uuid"]
    if ("idProject" in dictModel) and (dictModel["idProject"] != None):
      self.idProject = dictModel["idProject"]
    if ("idOwner" in dictModel) and (dictModel["idOwner"] != None):
      self.idOwner = dictModel["idOwner"]
    if ("advisorApproved" in dictModel) and (dictModel["advisorApproved"] != None):
      self.advisorApproved = dictModel["advisorApproved"]
    if ("uploadDate" in dictModel) and (dictModel["uploadDate"] != None):
      self.uploadDate = dictModel["uploadDate"]

  def __repr__(self):
    return '<Attachment idAttachment={} title={} uuid={} idProject={} idOwner={} advisorApproved={} uploadDate={} >'.format(self.idAttachment, self.title, self.uuid, self.idProject, self.idOwner, self.advisorApproved, self.uploadDate, )

  def json(self):
    return {
      "idAttachment":self.idAttachment,"title":self.title,"uuid":self.uuid,"idProject":self.idProject,"idOwner":self.idOwner,"advisorApproved":self.advisorApproved,"uploadDate":self.uploadDate,
    }

  def update(self, dictModel):
    if ("idAttachment" in dictModel) and (dictModel["idAttachment"] != None):
      self.idAttachment = dictModel["idAttachment"]
    if ("title" in dictModel) and (dictModel["title"] != None):
      self.title = dictModel["title"]
    if ("uuid" in dictModel) and (dictModel["uuid"] != None):
      self.uuid = dictModel["uuid"]
    if ("idProject" in dictModel) and (dictModel["idProject"] != None):
      self.idProject = dictModel["idProject"]
    if ("idOwner" in dictModel) and (dictModel["idOwner"] != None):
      self.idOwner = dictModel["idOwner"]
    if ("advisorApproved" in dictModel) and (dictModel["advisorApproved"] != None):
      self.advisorApproved = dictModel["advisorApproved"]
    if ("uploadDate" in dictModel) and (dictModel["uploadDate"] != None):
      self.uploadDate = dictModel["uploadDate"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Attachment).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Attachment).filter(Attachment.idAttachment == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getAttachment(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getAttachment(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Attachment).filter_by(**model).all()
  __db.session().commit()
  return results


def listAttachments():
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

def newAttachment(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Attachment(model)
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

def getAttachment(id):
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

def updateAttachment(id, model):
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

def deleteAttachment(id):
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

def findAttachment(model):
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