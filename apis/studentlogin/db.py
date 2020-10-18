import os
from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
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
  
def buildStudentRecordFromLDAPAttrs(attrs):
  return {
    'studentNumber': int(attrs['uid'][0].decode('utf-8')), 
    'email': f"{attrs['uid'][0].decode('utf-8')}@vnu.edu.vn",
    'fullname':attrs['cn'][0].decode('utf-8'), 
    'gender':True, 
    'dob': '2000-03-12'
  }

def doAuthenticate(uid, password):
  result = search('ou=dhcn,ou=sinhvien,dc=vnu,dc=vn', uid)
  if len(result) == 0:
    return False, "Student not found"
  dn, attrs = result[0]
  if authenticate(dn, password):
    return True, buildStudentRecordFromLDAPAttrs(attrs)
  else:
    return False, 'Login failed'

  # MOCK
  #return {'fullname': "Nguyen Van A", "gender": True, 'dob': '2000-03-12'}

def uidFromEmail(email):
  tokens = email.split('@')
  if len(tokens) != 2:
    raise BadRequest('Not valid email')
  return tokens[0]

def __doNew(instance):
  uid = uidFromEmail(instance.email)
  success, data = doAuthenticate(uid, instance.password)
  if not success:
    raise BadRequest(data)
  else:
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
      response.set_cookie('key', key, samesite='Lax', secure=True)
      response.set_cookie('jwt', jwt, samesite='Lax', secure=True)
      response.headers['x-key'] = key
      response.headers['x-jwt'] = jwt
      return response

    return student

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
