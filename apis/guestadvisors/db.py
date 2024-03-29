from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from ..sec_utils import isStaff, isIdGuestAdvisorMatched
from werkzeug.exceptions import *
from flask import session,request,after_this_request

from ..advisors import Advisor
__db = DbInstance.getInstance()



class Guestadvisor(__db.Base):
  __tablename__ = "guestadvisor"
  idGuestadvisor = Column(Integer, primary_key = True)
  email = Column(String(100))
  fullname = Column(String(200))
  affiliation = Column(String(255))
  password = Column(String(100))

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idGuestadvisor" in dictModel) and (dictModel["idGuestadvisor"] != None):
      self.idGuestadvisor = dictModel["idGuestadvisor"]
    if ("email" in dictModel) and (dictModel["email"] != None):
      self.email = dictModel["email"]
    if ("fullname" in dictModel) and (dictModel["fullname"] != None):
      self.fullname = dictModel["fullname"]
    if ("affiliation" in dictModel) and (dictModel["affiliation"] != None):
      self.affiliation = dictModel["affiliation"]
    if ("password" in dictModel) and (dictModel["password"] != None):
      self.password = dictModel["password"]

  def __repr__(self):
    return '<Guestadvisor idGuestadvisor={} email={} fullname={} affiliation={} password={} >'.format(self.idGuestadvisor, self.email, self.fullname, self.affiliation, self.password, )

  def json(self):
    return {
      "idGuestadvisor":self.idGuestadvisor,"email":self.email,"fullname":self.fullname,"affiliation":self.affiliation,"password":self.password,
    }

  def update(self, dictModel):
    if ("idGuestadvisor" in dictModel) and (dictModel["idGuestadvisor"] != None):
      self.idGuestadvisor = dictModel["idGuestadvisor"]
    if ("email" in dictModel) and (dictModel["email"] != None):
      self.email = dictModel["email"]
    if ("fullname" in dictModel) and (dictModel["fullname"] != None):
      self.fullname = dictModel["fullname"]
    if ("affiliation" in dictModel) and (dictModel["affiliation"] != None):
      self.affiliation = dictModel["affiliation"]
    if ("password" in dictModel) and (dictModel["password"] != None):
      self.password = dictModel["password"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Guestadvisor).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  doLog('__doNew____' + str(instance))
  email = instance.email
  fullname = instance.fullname
  try:
    __db.session().add(instance)
    __db.session().commit()
  except Exception as e:
    raise e

  advisor = Advisor({
    'email': email,
    'fullname': fullname,
    'idGuestadvisor': instance.idGuestadvisor
  })

  try:
    __db.session().add(advisor)
    __db.session().commit()
  except Exception as e:
    raise Exception(f'{e}')

  return instance

def __doGet(id):
  instance = __db.session().query(Guestadvisor).filter(Guestadvisor.idGuestadvisor == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getGuestadvisor(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getGuestadvisor(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Guestadvisor).filter_by(**model).all()
  __db.session().commit()
  return results


def listGuestadvisors():
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

def newGuestadvisor(model):
  doLog("new DAO function. model: {}".format(model))
  model['password'] = doHash(model['password'])
  instance = Guestadvisor(model)
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

def getGuestadvisor(id):
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

def updateGuestadvisor(id, model):
  doLog("update DAO function. Model: {}".format(model))
  try:
    if 'password' in model:
      model['password'] = doHash(model['password']);
    if isStaff(request, session) or isIdGuestAdvisorMatched(request, session, id):
      return __doUpdate(id, model)
    else:
      raise BadRequest("Not allowed")
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doUpdate(id, model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e
  except Exception as e:
    doLog(str(e))
    raise e

def deleteGuestadvisor(id):
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

def findGuestadvisor(model):
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
