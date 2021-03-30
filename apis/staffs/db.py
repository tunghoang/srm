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



class Staff(__db.Base):
  __tablename__ = "staff"
  idStaff = Column(Integer, primary_key = True)
  email = Column(String(100))
  fullname = Column(String(200))

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idStaff" in dictModel) and (dictModel["idStaff"] != None):
      self.idStaff = dictModel["idStaff"]
    if ("email" in dictModel) and (dictModel["email"] != None):
      self.email = dictModel["email"]
    if ("fullname" in dictModel) and (dictModel["fullname"] != None):
      self.fullname = dictModel["fullname"]

  def __repr__(self):
    return '<Staff idStaff={} email={} fullname={} >'.format(self.idStaff, self.email, self.fullname, )

  def json(self):
    return {
      "idStaff":self.idStaff,"email":self.email,"fullname":self.fullname,
    }

  def update(self, dictModel):
    if ("idStaff" in dictModel) and (dictModel["idStaff"] != None):
      self.idStaff = dictModel["idStaff"]
    if ("email" in dictModel) and (dictModel["email"] != None):
      self.email = dictModel["email"]
    if ("fullname" in dictModel) and (dictModel["fullname"] != None):
      self.fullname = dictModel["fullname"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Staff).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Staff).filter(Staff.idStaff == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getStaff(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getStaff(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Staff).filter_by(**model).all()
  __db.session().commit()
  return results


def listStaffs():
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

def newStaff(model):
  shouldBeStaff(request, session)
  doLog("new DAO function. model: {}".format(model))
  instance = Staff(model)
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

def getStaff(id):
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

def updateStaff(id, model):
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

def deleteStaff(id):
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

def findStaff(model):
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
