from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Advisor(__db.Base):
  __tablename__ = "advisor"
  idAdvisor = Column(Integer, primary_key = True)
  email = Column(String(100))
  fullname = Column(String(200))
  idQuota = Column(Integer, ForeignKey('quota.idQuota'))
  idGuestadvisor = Column(Integer, ForeignKey('guestadvisor.idGuestadvisor'))

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idAdvisor" in dictModel) and (dictModel["idAdvisor"] != None):
      self.idAdvisor = dictModel["idAdvisor"]
    if ("email" in dictModel) and (dictModel["email"] != None):
      self.email = dictModel["email"]
    if ("fullname" in dictModel) and (dictModel["fullname"] != None):
      self.fullname = dictModel["fullname"]
    if ("idQuota" in dictModel) and (dictModel["idQuota"] != None):
      self.idQuota = dictModel["idQuota"]
    if ("idGuestadvisor" in dictModel) and (dictModel["idGuestadvisor"] != None):
      self.idGuestadvisor = dictModel["idGuestadvisor"]

  def __repr__(self):
    return '<Advisor idAdvisor={} email={} fullname={} idQuota={} idGuestadvisor={} >'.format(self.idAdvisor, self.email, self.fullname, self.idQuota, self.idGuestadvisor, )

  def json(self):
    return {
      "idAdvisor":self.idAdvisor,"email":self.email,"fullname":self.fullname,"idQuota":self.idQuota,"idGuestadvisor":self.idGuestadvisor,
    }

  def update(self, dictModel):
    if ("idAdvisor" in dictModel) and (dictModel["idAdvisor"] != None):
      self.idAdvisor = dictModel["idAdvisor"]
    if ("email" in dictModel) and (dictModel["email"] != None):
      self.email = dictModel["email"]
    if ("fullname" in dictModel) and (dictModel["fullname"] != None):
      self.fullname = dictModel["fullname"]
    if ("idQuota" in dictModel) and (dictModel["idQuota"] != None):
      self.idQuota = dictModel["idQuota"]
    if ("idGuestadvisor" in dictModel) and (dictModel["idGuestadvisor"] != None):
      self.idGuestadvisor = dictModel["idGuestadvisor"]

def __recover():
  __db.newSession()

def __doList():
  return __db.session().query(Advisor).all()
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  queryStr = """
    SELECT a.idAdvisor, a.fullname, a.email, a.idGuestadvisor, g.affiliation
    FROM advisor a 
      LEFT JOIN guestadvisor g 
        ON a.idGuestadvisor = g.idGuestadvisor
    WHERE a.idAdvisor = :idAdvisor
  """
  params = {'idAdvisor': id}
  result = __db.session().execute(queryStr, params).fetchone()
  return {
    'idAdvisor': result[0], 
    'fullname': result[1],
    'email': result[2],
    'idGuestadvisor': result[3],
    'affiliation': result[4]
  }
  #instance = __db.session().query(Advisor).filter(Advisor.idAdvisor == id).scalar()
  #doLog("__doGet: {}".format(instance))
  #return instance

def __doUpdate(id, model):
  #instance = getAdvisor(id)
  instance = __db.session().query(Advisor).filter(Advisor.idAdvisor == id).scalar()
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  #instance = getAdvisor(id)
  instance = __db.session().query(Advisor).filter(Advisor.idAdvisor == id).scalar()
  idGuestAdvisor = instance.idGuestadvisor  
  __db.session().delete(instance)
  __db.session().commit()
  return instance

def __doFind(model):
  if 'email' in model:
    results = __db.session().query(Advisor).filter(Advisor.email.ilike(f"%{model['email']}%")).all()
  elif 'fullname' in model:
    results = __db.session().query(Advisor).filter(Advisor.fullname.ilike(f"%{model['fullname']}%")).all()
  else:
    results = __db.session().query(Advisor).filter_by(**model).all()
  return results


def listAdvisors():
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

def newAdvisor(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Advisor(model)
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

def getAdvisor(id):
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

def updateAdvisor(id, model):
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

def deleteAdvisor(id):
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

def findAdvisor(model):
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

def __doDump():
  queryStr = """
    SELECT a.idAdvisor, a.fullname, a.email, a.idGuestadvisor, g.affiliation
    FROM advisor a 
      LEFT JOIN guestadvisor g 
        ON a.idGuestadvisor = g.idGuestadvisor
  """
  results = __db.session().execute(queryStr).fetchall()
  return list(map(lambda result: {
    'idAdvisor': result[0], 
    'fullname': result[1],
    'email': result[2],
    'idGuestadvisor': result[3],
    'affiliation': result[4]
  }, results))
  
def dumpAdvisors():
  doLog('dump Advisor')
  try:
    return __doDump()
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doDump(model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e
