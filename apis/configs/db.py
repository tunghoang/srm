from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Config(__db.Base):
  __tablename__ = "config"
  idConfig = Column(Integer, primary_key = True)
  key = Column(String(50))
  value = Column(String(50))

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idConfig" in dictModel) and (dictModel["idConfig"] != None):
      self.idConfig = dictModel["idConfig"]
    if ("key" in dictModel) and (dictModel["key"] != None):
      self.key = dictModel["key"]
    if ("value" in dictModel) and (dictModel["value"] != None):
      self.value = dictModel["value"]

  def __repr__(self):
    return '<Config idConfig={} key={} value={} >'.format(self.idConfig, self.key, self.value, )

  def json(self):
    return {
      "idConfig":self.idConfig,"key":self.key,"value":self.value,
    }

  def update(self, dictModel):
    if ("idConfig" in dictModel) and (dictModel["idConfig"] != None):
      self.idConfig = dictModel["idConfig"]
    if ("key" in dictModel) and (dictModel["key"] != None):
      self.key = dictModel["key"]
    if ("value" in dictModel) and (dictModel["value"] != None):
      self.value = dictModel["value"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Config).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Config).filter(Config.idConfig == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getConfig(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getConfig(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Config).filter_by(**model).all()
  __db.session().commit()
  return results


def listConfigs():
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

def newConfig(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Config(model)
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

def getConfig(id):
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

def updateConfig(id, model):
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

def deleteConfig(id):
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

def findConfig(model):
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
