import os
from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request
from ..advisors import Advisor
from ..ldap import search,authenticate

__db = DbInstance.getInstance()


class Advisorlogin:
  email = Column(String)
  password = Column(String)

  def __init__(self, dictModel):
    if ("email" in dictModel) and (dictModel["email"] != None):
      self.email = dictModel["email"]
    if ("password" in dictModel) and (dictModel["password"] != None):
      self.password = dictModel["password"]

  def __repr__(self):
    return '<Advisorlogin email={} password={} >'.format(self.email, self.password, )

  def json(self):
    return {
      "email":self.email, "password": self.password,
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
  
def doAuthenticate(uid, password):
  result = search('ou=dhcn,ou=canbo,dc=vnu,dc=vn', uid)
  if len(result) == 0:
    return False, "Account not found"
  dn, attrs = result[0]
  if authenticate(dn, password):
    return True, buildAdvisorRecordFromLDAPAttrs(attrs)
  else:
    return False, 'Login failed'

def __doNew(instance):
  uid = uidFromEmail(instance.email)
  success, data = doAuthenticate(uid, instance.password)
  if not success:
    raise BadRequest(data)
  else:
    advisorRecord = data
    advisor = __db.session().query(Advisor).filter(Advisor.email == instance.email).first()
    if advisor is None:
      advisor = Advisor({
        'email': instance.email,
        'fullname': advisorRecord['fullname'],
        'idQuota': advisorRecord['idQuota'],
        'idGuestadvisor': advisorRecord['idGuestadvisor']
      })
      __db.session().add(advisor)
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


def listAdvisorlogins():
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

def newAdvisorlogin(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Advisorlogin(model)
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

def getAdvisorlogin(id):
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

def updateAdvisorlogin(id, model):
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

def deleteAdvisorlogin(id):
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

def findAdvisorlogin(model):
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
