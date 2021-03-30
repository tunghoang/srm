from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

from ..sec_utils import *

__db = DbInstance.getInstance()



class Klass(__db.Base):
  __tablename__ = "klass"
  idKlass = Column(Integer, primary_key = True)
  className = Column(String(100))
  category = Column(String(50))

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idKlass" in dictModel) and (dictModel["idKlass"] != None):
      self.idKlass = dictModel["idKlass"]
    if ("className" in dictModel) and (dictModel["className"] != None):
      self.className = dictModel["className"]
    if ("category" in dictModel) and (dictModel["category"] != None):
      self.category = dictModel["category"]

  def __repr__(self):
    return '<Klass idKlass={} className={} category={} >'.format(self.idKlass, self.className, self.category, )

  def json(self):
    return {
      "idKlass":self.idKlass,"className":self.className,"category":self.category,
    }

  def update(self, dictModel):
    if ("idKlass" in dictModel) and (dictModel["idKlass"] != None):
      self.idKlass = dictModel["idKlass"]
    if ("className" in dictModel) and (dictModel["className"] != None):
      self.className = dictModel["className"]
    if ("category" in dictModel) and (dictModel["category"] != None):
      self.category = dictModel["category"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Klass).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Klass).filter(Klass.idKlass == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getKlass(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getKlass(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Klass).filter_by(**model).all()
  __db.session().commit()
  return results


def listKlasss():
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

def newKlass(model):
  shouldBeStaff(request, session)
  doLog("new DAO function. model: {}".format(model))
  instance = Klass(model)
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

def getKlass(id):
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

def updateKlass(id, model):
  shouldBeStaff(request, session)
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

def deleteKlass(id):
  shouldBeStaff(request, session)
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

def findKlass(model):
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
