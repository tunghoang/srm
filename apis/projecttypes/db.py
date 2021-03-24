from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Projecttype(__db.Base):
  __tablename__ = "projecttype"
  idProjecttype = Column(Integer, primary_key = True)
  name = Column(String(30))
  description = Column(String(255))

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idProjecttype" in dictModel) and (dictModel["idProjecttype"] != None):
      self.idProjecttype = dictModel["idProjecttype"]
    if ("name" in dictModel) and (dictModel["name"] != None):
      self.name = dictModel["name"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]

  def __repr__(self):
    return '<Projecttype idProjecttype={} name={} description={} >'.format(self.idProjecttype, self.name, self.description, )

  def json(self):
    return {
      "idProjecttype":self.idProjecttype,"name":self.name,"description":self.description,
    }

  def update(self, dictModel):
    if ("idProjecttype" in dictModel) and (dictModel["idProjecttype"] != None):
      self.idProjecttype = dictModel["idProjecttype"]
    if ("name" in dictModel) and (dictModel["name"] != None):
      self.name = dictModel["name"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Projecttype).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Projecttype).filter(Projecttype.idProjecttype == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getProjecttype(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getProjecttype(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Projecttype).filter_by(**model).all()
  __db.session().commit()
  return results


def listProjecttypes():
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

def newProjecttype(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Projecttype(model)
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

def getProjecttype(id):
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

def updateProjecttype(id, model):
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

def deleteProjecttype(id):
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

def findProjecttype(model):
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